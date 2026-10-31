# Додаток Г. Довідник рецептів коду – приклад 7 (рукопис: 93-dodatok-g.md, рядок 106)
import asyncio

async def classify_all(claims: list[str]) -> list[str]:
    gate = asyncio.Semaphore(5)              # не більше 5 запитів одночасно

    async def one(text: str) -> str:
        async with gate:
            r = await client.aio.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f"Категорія претензії одним словом: {text}")
            return r.text or "невідомо"

    return await asyncio.gather(*(one(c) for c in claims))

print(asyncio.run(classify_all(["Пошкоджено палету", "Запізнення на 3 дні"])))
