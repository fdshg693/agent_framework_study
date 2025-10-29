import asyncio
from typing import cast

from agent_framework import ChatMessage, ConcurrentBuilder, WorkflowOutputEvent, ChatAgent
from agent_framework.openai import OpenAIResponsesClient
from typing import Annotated
from pydantic import Field

from agent_framework import AgentMiddleware, AgentRunContext, ChatAgent


class LoggingMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    async def process(self, context: AgentRunContext, next):
        print("Starting agent run with LoggingMiddleware")
        await next(context)

async def middleware_example():
    client = OpenAIResponsesClient(model_id="gpt-5-nano")

    simple: ChatAgent = client.create_agent(
        instructions="1+1",
        name="simple",
        middleware=LoggingMiddleware(max_retries=2),
    )

    result = await simple.run(messages=[ChatMessage(role="user", text="What is the square of 4?")])
    print(result.text)

def get_square(
    num: Annotated[str, Field(description="number for square.")],
) -> str:
    """Get the square of a given number."""
    print(f"Calculating the square of {num}")
    try:
        n = int(num)
        return f"The square of {n} is {n * n}."
    except ValueError:
        return "Please provide a valid integer."

async def single_agent_example():
    prompt ="what is the square of 5?"
    client = OpenAIResponsesClient(model_id="gpt-5-nano")

    math: ChatAgent = client.create_agent(
        instructions=("call the tool to compute the square of a number "),
        name="math",
        tools=[get_square],
    )

    result = await math.run(messages=[ChatMessage(role="user", text=prompt)])
    print(result.text)

if __name__ == "__main__":
    asyncio.run(middleware_example())