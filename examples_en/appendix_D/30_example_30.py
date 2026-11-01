# Appendix D. Code Recipes – example 30 (manuscript: 93-appendix-d.md, line 592)
for level in ["MEDIA_RESOLUTION_LOW", "MEDIA_RESOLUTION_HIGH"]:
    image = types.Part.from_bytes(data=photo, mime_type="image/jpeg", media_resolution=level)
    n = client.models.count_tokens(model="gemini-3.8-flash", contents=[image, "Waybill number?"])
    print(level, n.total_tokens)

SYSTEM = "You are Trembita, the assistant of the Smereka company."
print(client.models.count_tokens(model="gemini-3.8-flash", contents=SYSTEM).total_tokens)
# config=types.CountTokensConfig(system_instruction=SYSTEM) outside Agent Platform – ValueError
