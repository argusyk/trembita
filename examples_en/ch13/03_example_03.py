# Chapter 13. Optimization: context caching, batch processing and cost – example 3 (manuscript: 13-optymizatsiya.md, line 158)
import datetime as dt
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

client = genai.Client()
with open("reglament_smereka.md", encoding="utf-8") as f:
    REGULATIONS = f.read()

cache = client.caches.create(
    model=MODEL_MAIN,                       # the cache is bound to a specific model
    config=types.CreateCachedContentConfig(
        display_name="reglament-smereka-2026-10",
        system_instruction=SYSTEM_INSTRUCTION,
        contents=[types.Content(role="user", parts=[types.Part(text=REGULATIONS)])],
        ttl="3600s",                        # one hour; a duration is a string with the suffix s
    ),
)
resp = client.models.generate_content(
    model=MODEL_MAIN,                       # the same model as in the cache
    contents="What is the deadline for filing a claim for damaged cargo?",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print(resp.text, "| from cache:", resp.usage_metadata.cached_content_token_count)

# Extend by two more hours or until the end of the shift: 19:00 Kyiv time (17:00 UTC in winter, 16:00 in summer)
client.caches.update(name=cache.name, config=types.UpdateCachedContentConfig(ttl="7200s"))
end = dt.datetime(2026, 11, 2, 19, 0, tzinfo=ZoneInfo("Europe/Kyiv"))
client.caches.update(name=cache.name,
                     config=types.UpdateCachedContentConfig(expire_time=end.astimezone(dt.timezone.utc)))

for c in client.caches.list():              # forgotten caches: money leaking every hour
    print(c.display_name, c.model, c.expire_time)
client.caches.delete(name=cache.name)       # the shift is over: we do not pay at night
