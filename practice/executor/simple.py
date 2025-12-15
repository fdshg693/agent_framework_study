import asyncio

from agent_framework import (
    handler,
    Executor,
    ChatClientProtocol,
    WorkflowContext,
    SharedState,
    InProcRunnerContext,
)
from agent_framework.openai import OpenAIChatClient


class NumberDoubleExecutor(Executor):
    """Executor that doubles the input number."""

    def __init__(self, id: str, chat_client: ChatClientProtocol) -> None:
        super().__init__(id=id)
        self._chat_client = chat_client

    @handler
    async def handle_user_messages(
        self, user_messages: str, ctx: WorkflowContext[str]
    ) -> None:
        input_number = int(user_messages[-1])

        doubled_number = input_number * 2
        print(f"Doubled number: {doubled_number}")
        await ctx.send_message(str(doubled_number))
        return


chat_client = OpenAIChatClient(model_id="gpt-4o-mini")

number_double_executor = NumberDoubleExecutor(
    id="number_double_executor", chat_client=chat_client
)


async def main():
    runner_context = InProcRunnerContext()
    if number_double_executor.can_handle("5"):
        await number_double_executor.execute(
            message="5",
            source_executor_ids="number_double_executor",
            shared_state=SharedState(),
            runner_context=runner_context,
        )
    else:
        print("Executor cannot handle the input.")

    messages = await runner_context.drain_messages()
    print("Messages exchanged during execution:", messages)


if __name__ == "__main__":
    asyncio.run(main())
