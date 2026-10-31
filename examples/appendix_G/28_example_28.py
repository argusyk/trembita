# Додаток Г. Довідник рецептів коду – приклад 28 (рукопис: 93-dodatok-g.md, рядок 547)
REGULATIONS = open("reglament_smereka.md", encoding="utf-8").read()   # ~120 тис. токенів
cache = client.caches.create(
    model="gemini-3.8-flash",                    # кеш прив'язаний до моделі
    config=types.CreateCachedContentConfig(
        system_instruction="Ти – «Трембіта», асистент компанії «Смерека».",
        contents=[types.Content(role="user", parts=[types.Part(text=REGULATIONS)])],
        ttl="3600s"),                            # рядок із суфіксом s
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",                    # та сама модель, що й у кеші
    contents="Який строк подання претензії на пошкоджений вантаж?",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print("з кешу:", resp.usage_metadata.cached_content_token_count)
client.caches.delete(name=cache.name)            # зберігання оплачується щогодини
