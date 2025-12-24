# https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/chat_client/azure_ai_chat_client.py

import asyncio

from agent_framework.azure import AzureOpenAIChatClient


async def main() -> None:
    # env_file_pathの内容の読み込みはPydanticが裏側で使われている
    # 詳細は zenn/docs/SettingsConfigDict.md を参照
    client = AzureOpenAIChatClient(env_file_path=".env")
    message = "1+1=?"
    print(f"User: {message}")
    response = await client.get_response(message)
    print(f"Assistant: {response}")


if __name__ == "__main__":
    asyncio.run(main())
