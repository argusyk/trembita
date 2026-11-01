# Chapter 10. Function Calling – example 8 (manuscript: 10-funktsii.md, line 341)
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
                config=types.GenerateContentConfig(tools=[session]),   # MCP session as a tool
            )
            return resp.text

print(asyncio.run(ask_with_mcp("Where is SM-2610-0042 and until what time is the Uzhhorod warehouse open?")))
