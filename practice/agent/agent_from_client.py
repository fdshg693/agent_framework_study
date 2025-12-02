from agent_framework.openai import OpenAIResponsesClient

# Create a client
client = OpenAIResponsesClient(model_id="gpt-5-nano")

# Create an agent using the convenience method
agent = client.create_agent(
    name="assistant", instructions="You are a helpful assistant."
)


async def get_response():
    # Run the agent
    response = await agent.run("Hello!")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_response())
