# Розділ 7. Gemini API і Google Gen AI SDK – приклад 6 (рукопис: 07-api.md, рядок 271)
import asyncio
from google import genai

client = genai.Client()

# Синхронний потік: друкуємо фрагменти в міру надходження
usage = None
for chunk in client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="Поясни водієві, як оформити ТТН на збірний вантаж.",
):
    if chunk.text:                       # службовий фрагмент може не мати тексту
        print(chunk.text, end="", flush=True)
    usage = chunk.usage_metadata or usage
print("\nвихідних токенів:", usage.candidates_token_count if usage else "?")


# Асинхронно: класифікуємо претензії паралельно, але не більше 5 одночасно
async def classify_all(claims: list[str]) -> list[str]:
    gate = asyncio.Semaphore(5)          # бережемо квоту запитів на хвилину

    async def one(text: str) -> str:
        async with gate:
            r = await client.aio.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f"Категорія претензії одним словом: {text}",
            )
            return r.text or "невідомо"

    return await asyncio.gather(*(one(c) for c in claims))

print(asyncio.run(classify_all(["Пошкоджено палету", "Запізнення на 3 дні"])))
