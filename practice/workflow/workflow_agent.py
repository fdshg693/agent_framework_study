import asyncio
from dataclasses import dataclass
from uuid import uuid4

from agent_framework import (
    AgentRunResponse,
    WorkflowBuilder,
    ChatAgent,
    Executor,
    handler,
    ChatClientProtocol,
    ChatMessage,
    WorkflowContext,
    Role,
)
from agent_framework.openai import OpenAIChatClient
from pydantic import BaseModel


class NumberDoubler(Executor):
    """Executor that doubles the input number."""

    def __init__(self, id: str, chat_client: ChatClientProtocol) -> None:
        super().__init__(id=id)
        self._chat_client = chat_client

    @handler
    async def handle_user_messages(
        self, user_messages: list[ChatMessage], ctx: WorkflowContext[int]
    ) -> None:
        input_number = int(user_messages[-1].text)

        print(input_number * 2)
        return


chat_client = OpenAIChatClient(model_id="gpt-4o-mini")

number_doubler = NumberDoubler(id="number_doubler", chat_client=chat_client)

workflow_agent = (
    WorkflowBuilder()
    .set_start_executor(number_doubler)
    .build()
    .as_agent()  # Wrap workflow as an agent
)

input_number = "5"


async def main():
    response: AgentRunResponse = await workflow_agent.run(input_number)

    print("Final Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
