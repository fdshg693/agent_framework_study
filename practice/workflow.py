import asyncio
from dataclasses import dataclass
from uuid import uuid4

from agent_framework import (
    AgentRunResponseUpdate,
    AgentRunUpdateEvent,
    ChatClientProtocol,
    ChatMessage,
    Contents,
    Executor,
    Role,
    WorkflowBuilder,
    WorkflowContext,
    handler,
)
from agent_framework.openai import OpenAIChatClient
from pydantic import BaseModel

@dataclass
class ReviewRequest:
    """Structured request passed from Worker to Reviewer for evaluation."""

    request_id: str
    user_messages: list[ChatMessage]
    agent_messages: list[ChatMessage]


@dataclass
class ReviewResponse:
    """Structured response from Reviewer back to Worker."""

    request_id: str
    feedback: str
    approved: bool


class AutoApprover(Executor):
    """Executor that reviews agent responses and provides structured feedback."""

    def __init__(self, id: str) -> None:
        super().__init__(id=id)

    @handler
    async def review(self, request: ReviewRequest, ctx: WorkflowContext[ReviewResponse]) -> None:

        print(f"Reviewer: Reviewing requested")
        print(f"USER:{request.user_messages[-1].text}")
        print(f"AGENT:{request.agent_messages[-1].text}")

        await ctx.send_message(
            ReviewResponse(request_id=request.request_id, feedback="OK", approved=True)
        )

class SecondApprover(Executor):
    """Executor that reviews agent responses and provides structured feedback."""

    def __init__(self, id: str) -> None:
        super().__init__(id=id)
        self.review_count = 0

    @handler
    async def review(self, request: ReviewRequest, ctx: WorkflowContext[ReviewResponse]) -> None:

        print(f"Reviewer: Reviewing requested")
        print(f"USER:{request.user_messages[-1].text}")
        print(f"AGENT:{request.agent_messages[-1].text}")

        # Reject the first review to demonstrate feedback incorporation.
        if self.review_count < 1:
            await ctx.send_message(
                ReviewResponse(request_id=request.request_id, feedback="use easier words", approved=False)                
            )
            self.review_count += 1
        else:
            await ctx.send_message(
                ReviewResponse(request_id=request.request_id, feedback="OK", approved=True)
            )



class Worker(Executor):
    """Executor that generates responses and incorporates feedback when necessary."""

    def __init__(self, id: str, chat_client: ChatClientProtocol) -> None:
        super().__init__(id=id)
        self._chat_client = chat_client
        self._pending_requests: dict[str, tuple[ReviewRequest, list[ChatMessage]]] = {}

    @handler
    async def handle_user_messages(self, user_messages: list[ChatMessage], ctx: WorkflowContext[ReviewRequest]) -> None:

        messages = [ChatMessage(role=Role.SYSTEM, text="You are a helpful assistant.")]
        messages.extend(user_messages)

        response = await self._chat_client.get_response(messages=messages)
        print(f"Worker: Response generated: {response.messages[-1].text}")

        # Add agent messages to context.
        messages.extend(response.messages)

        # Create review request and send to Reviewer.
        request = ReviewRequest(request_id=str(uuid4()), user_messages=user_messages, agent_messages=response.messages)
        print(f"Worker: Sending response for review (ID: {request.request_id[:8]})")
        await ctx.send_message(request)

        # Track request for possible retry.
        self._pending_requests[request.request_id] = (request, messages)

    @handler
    async def handle_review_response(self, review: ReviewResponse, ctx: WorkflowContext[ReviewRequest]) -> None:
        print(f"Worker: Received review for request {review.request_id[:8]} - Approved: {review.approved}")

        if review.request_id not in self._pending_requests:
            raise ValueError(f"Unknown request ID in review: {review.request_id}")

        request, messages = self._pending_requests.pop(review.request_id)

        if review.approved:
            print("Worker: Response approved. Emitting to external consumer...")
            contents: list[Contents] = []
            for message in request.agent_messages:
                contents.extend(message.contents)

            # Emit approved result to external consumer via AgentRunUpdateEvent.
            await ctx.add_event(
                AgentRunUpdateEvent(self.id, data=AgentRunResponseUpdate(contents=contents, role=Role.ASSISTANT))
            )
            return

        print(f"Worker: Response not approved. Feedback: {review.feedback}")

        # Incorporate review feedback.
        messages.append(ChatMessage(role=Role.SYSTEM, text=review.feedback))
        messages.append(
            ChatMessage(role=Role.SYSTEM, text="Please incorporate the feedback and regenerate the response.")
        )
        messages.extend(request.user_messages)

        # Retry with updated prompt.
        response = await self._chat_client.get_response(messages=messages)
        print(f"Worker: New response generated: {response.messages[-1].text}")

        messages.extend(response.messages)

        # Send updated request for re-review.
        new_request = ReviewRequest(
            request_id=review.request_id, user_messages=request.user_messages, agent_messages=response.messages
        )
        await ctx.send_message(new_request)

        # Track new request for further evaluation.
        self._pending_requests[new_request.request_id] = (new_request, messages)


async def main() -> None:

    # Initialize chat clients and executors.
    mini_chat_client = OpenAIChatClient(model_id="gpt-4.1-nano")
    reviewer = SecondApprover(id="reviewer")
    worker = Worker(id="worker", chat_client=mini_chat_client)

    agent = (
        WorkflowBuilder()
        .add_edge(worker, reviewer)  # Worker sends responses to Reviewer
        .add_edge(reviewer, worker)  # Reviewer provides feedback to Worker
        .set_start_executor(worker)
        .build()
        .as_agent()  # Wrap workflow as an agent
    )

    query = "write simple sonnet in 30 words, and submit for review"

    async for event in agent.run_stream(
        query
    ):
        print(f"Agent Response: {event}")


if __name__ == "__main__":
    asyncio.run(main())