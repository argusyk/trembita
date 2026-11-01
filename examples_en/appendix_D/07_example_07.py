# Appendix D. Code Recipes – example 7 (manuscript: 93-appendix-d.md, line 106)
import asyncio

async def classify_all(claims: list[str]) -> list[str]:
    gate = asyncio.Semaphore(5)              # no more than 5 requests at a time

    async def one(text: str) -> str:
        async with gate:
            r = await client.aio.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f"Claim category in one word: {text}")
            return r.text or "unknown"

    return await asyncio.gather(*(one(c) for c in claims))

print(asyncio.run(classify_all(["Pallet damaged", "Delivered 3 days late"])))
