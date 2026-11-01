# Chapter 7. The Gemini API and the Google Gen AI SDK – example 6 (manuscript: 07-api.md, line 271)
import asyncio
from google import genai

client = genai.Client()

# Synchronous stream: print the fragments as they arrive
usage = None
for chunk in client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="Explain to a driver how to fill in a TTN waybill for a groupage shipment.",
):
    if chunk.text:                       # a service fragment may have no text
        print(chunk.text, end="", flush=True)
    usage = chunk.usage_metadata or usage
print("\noutput tokens:", usage.candidates_token_count if usage else "?")


# Asynchronously: classify claims concurrently, but no more than 5 at a time
async def classify_all(claims: list[str]) -> list[str]:
    gate = asyncio.Semaphore(5)          # protect the requests-per-minute quota

    async def one(text: str) -> str:
        async with gate:
            r = await client.aio.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f"Claim category in one word: {text}",
            )
            return r.text or "unknown"

    return await asyncio.gather(*(one(c) for c in claims))

print(asyncio.run(classify_all(["Pallet damaged", "Delivered 3 days late"])))
