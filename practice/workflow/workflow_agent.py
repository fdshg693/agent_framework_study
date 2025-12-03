import asyncio

from agent_framework import (
    AgentRunResponse,
    WorkflowBuilder,
    Executor,
    ChatClientProtocol,
    ChatMessage,
    WorkflowContext,
    handler,
)
from agent_framework.openai import OpenAIChatClient


class NumberDoubleExecutor(Executor):
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

number_double_executor = NumberDoubleExecutor(
    id="number_double_executor", chat_client=chat_client
)

workflow = WorkflowBuilder().set_start_executor(number_double_executor).build()


async def main(input_number: str = "5"):
    response: AgentRunResponse = await workflow.run(input_number)

    print("Final Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
