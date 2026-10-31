# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 3 (рукопис: 13-optymizatsiya.md, рядок 144)
import datetime as dt
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

client = genai.Client()
with open("reglament_smereka.md", encoding="utf-8") as f:
    REGULATIONS = f.read()

cache = client.caches.create(
    model=MODEL_MAIN,                       # кеш прив'язаний до конкретної моделі
    config=types.CreateCachedContentConfig(
        display_name="reglament-smereka-2026-10",
        system_instruction=SYSTEM_INSTRUCTION,
        contents=[types.Content(role="user", parts=[types.Part(text=REGULATIONS)])],
        ttl="3600s",                        # година; тривалість – рядок із суфіксом s
    ),
)
resp = client.models.generate_content(
    model=MODEL_MAIN,                       # та сама модель, що й у кеші
    contents="Який строк подання претензії на пошкоджений вантаж?",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print(resp.text, "| з кешу:", resp.usage_metadata.cached_content_token_count)

# Подовжити ще на дві години або до кінця зміни (19:00 за Києвом = 17:00 UTC взимку)
client.caches.update(name=cache.name, config=types.UpdateCachedContentConfig(ttl="7200s"))
end = dt.datetime(2026, 11, 2, 17, 0, tzinfo=dt.timezone.utc)
client.caches.update(name=cache.name, config=types.UpdateCachedContentConfig(expire_time=end))

for c in client.caches.list():              # забуті кеші – гроші, що витікають щогодини
    print(c.display_name, c.model, c.expire_time)
client.caches.delete(name=cache.name)       # зміна закінчилася – вночі не платимо
