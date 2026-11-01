# Appendix D. Code Recipes – example 28 (manuscript: 93-appendix-d.md, line 547)
REGULATIONS = open("reglament_smereka.md", encoding="utf-8").read()   # ~120 thousand tokens
cache = client.caches.create(
    model="gemini-3.8-flash",                    # the cache is bound to the model
    config=types.CreateCachedContentConfig(
        system_instruction="You are Trembita, the assistant of the Smereka company.",
        contents=[types.Content(role="user", parts=[types.Part(text=REGULATIONS)])],
        ttl="3600s"),                            # a string with the suffix s
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",                    # the same model as in the cache
    contents="What is the deadline for filing a claim for damaged cargo?",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print("from cache:", resp.usage_metadata.cached_content_token_count)
client.caches.delete(name=cache.name)            # storage is billed hourly
