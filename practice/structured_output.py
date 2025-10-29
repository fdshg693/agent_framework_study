import asyncio

from agent_framework import AgentRunResponse
from agent_framework.openai import OpenAIResponsesClient
from pydantic import BaseModel

class Language(BaseModel):
    """A structured output for testing purposes."""

    language: str
    difficulty: str


async def simple_structure_example() -> None:

    agent = OpenAIResponsesClient(model_id="gpt-5-nano").create_agent(
        name="CityAgent",
        instructions="Determine the language, and its difficulty level from the given text.",
    )

    query = "Ich bin in Paris."
    print(f"User: {query}")

    result = await agent.run(query, response_format=Language)

    if result.value:
        structured_data: Language = result.value  # type: ignore
        print("Assistant Structured Output:")
        print(f"Language: {structured_data.language}")
        print(f"Difficulty: {structured_data.difficulty}")
    else:
        print("Error: No structured data found in result.value")

async def main() -> None:

    await simple_structure_example()


if __name__ == "__main__":
    asyncio.run(main())