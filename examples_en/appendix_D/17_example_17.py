# Appendix D. Code Recipes – example 17 (manuscript: 93-appendix-d.md, line 314)
photo = open("cmr_SM-2610-0042.jpg", "rb").read()
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        types.Part.from_bytes(data=photo, mime_type="image/jpeg",
            media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH),
        "What document is this? List the filled-in boxes and mark the illegible ones.",
    ],
)
print(resp.text, resp.usage_metadata.prompt_token_count)
