# Appendix D. Code Recipes – example 16 (manuscript: 93-appendix-d.md, line 289)
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python", args=["-m", "smereka_mcp.server"])

async def ask_with_mcp(question: str) -> str:
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            resp = await client.aio.models.generate_content(
                model="gemini-3.8-flash", contents=question,
                config=types.GenerateContentConfig(tools=[session]))
            return resp.text

print(asyncio.run(ask_with_mcp("Where is SM-2610-0042?")))
