from agent_framework import BaseChatClient, ChatResponse, ChatMessage, ChatAgent, BaseAgent, AgentRunResponse, AgentRunResponseUpdate

class CustomChatClient(BaseChatClient):
    async def _inner_get_response(self, *, messages, chat_options, **kwargs):
        # Your custom implementation
        return ChatResponse(
            messages=[ChatMessage(role="assistant", text="2")], response_id="custom-response"
        )

    async def _inner_get_streaming_response(self, *, messages, chat_options, **kwargs):
        # Your custom streaming implementation
        from agent_framework import ChatResponseUpdate

        yield ChatResponseUpdate(role="assistant", contents=[{"type": "text", "text": "2"}])
        yield ChatResponseUpdate(role="assistant", contents=[{"type": "text", "text": "And that is 1+1."}])

class SimpleAgent(BaseAgent):
    async def run(self, messages=None, *, thread=None, **kwargs):
        # Custom implementation
        msg = ChatMessage(role="assistant", text="This is a simple agent.")
        return AgentRunResponse(messages=[msg], response_id="simple-response")

    def run_stream(self, messages=None, *, thread=None, **kwargs):
        async def _stream():
            # Custom streaming implementation
            yield AgentRunResponseUpdate()

        return _stream()

async def run_agent_example():
    # Create an instance of your custom client
    custom_client = CustomChatClient()

    # Create a basic chat agent
    agent = ChatAgent(chat_client=custom_client, name="assistant", description="A helpful assistant")

    # Run the agent with a simple message
    response = await agent.run("Hello, how are you?")
    print(response.text)

async def run_simple_agent_example():
    # Create a simple agent
    agent = SimpleAgent(name="my-agent", description="A simple agent implementation")

    # Run the simple agent with a message
    response = await agent.run("Hello, simple agent!")
    print(response.text)

if __name__ == "__main__":
    import asyncio
    # asyncio.run(run_agent_example())
    asyncio.run(run_simple_agent_example())