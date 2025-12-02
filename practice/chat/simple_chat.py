from agent_framework import BaseChatClient, ChatResponse, ChatMessage
from agent_framework.openai import OpenAIResponsesClient


class CustomChatClient(BaseChatClient):
    async def _inner_get_response(self, *, messages, chat_options, **kwargs):
        # Your custom implementation
        return ChatResponse(
            messages=[ChatMessage(role="assistant", text="2")],
            response_id="custom-response",
        )

    async def _inner_get_streaming_response(self, *, messages, chat_options, **kwargs):
        # Your custom streaming implementation
        from agent_framework import ChatResponseUpdate

        yield ChatResponseUpdate(
            role="assistant", contents=[{"type": "text", "text": "2"}]
        )
        yield ChatResponseUpdate(
            role="assistant", contents=[{"type": "text", "text": "And that is 1+1."}]
        )


# Create an instance of your custom client
custom_client = CustomChatClient()

openai_client = OpenAIResponsesClient(model_id="gpt-5-nano")


async def get_custom_response():
    # Use the client to get responses
    response = await custom_client.get_response("1+1")
    print(response)


async def get_custom_streaming_response():
    # Use the client to get streaming responses
    async for chunk in custom_client.get_streaming_response("1+1"):
        print(chunk)


async def get_openai_response():
    # Use the OpenAI client to get responses
    response = await openai_client.get_response("1+1")
    print(response)


def print_client_info():
    client_info = openai_client.to_dict()
    print(client_info)


if __name__ == "__main__":
    # import asyncio
    # asyncio.run(get_openai_response())
    print_client_info()
