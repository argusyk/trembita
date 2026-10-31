# Розділ 10. Виклик функцій – приклад 8 (рукопис: 10-funktsii.md, рядок 331)
import asyncio
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python", args=["-m", "smereka_mcp.server"])

async def ask_with_mcp(question: str) -> str:
    client = genai.Client()
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            resp = await client.aio.models.generate_content(
                model="gemini-3.8-flash",
                contents=question,
                config=types.GenerateContentConfig(tools=[session]),   # сесія MCP як інструмент
            )
            return resp.text

print(asyncio.run(ask_with_mcp("Де SM-2610-0042 і до якої години працює склад в Ужгороді?")))
