from agent_framework import BaseChatClient, ChatResponse, ChatMessage, ChatAgent


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

# Create an agent
agent = ChatAgent(
    chat_client=custom_client,
    name="custom_agent",
    description="A custom agent that answers simple math questions",
)

# Convert the agent to a tool
custom_agent_tool = agent.as_tool()


async def main():
    result = await custom_agent_tool.invoke(query="What is 1+1?")
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
