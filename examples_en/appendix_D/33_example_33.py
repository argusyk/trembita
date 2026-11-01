# Appendix D. Code Recipes – example 33 (manuscript: 93-appendix-d.md, line 662)
resp = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents="Diagram for drivers: how to secure pallets with straps. Light background, no text.",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9")),
)
for i, part in enumerate(resp.parts or []):     # None if the request was blocked
    if part.inline_data:
        part.as_image().save(f"kriplennia_{i}.png")
    elif part.text:
        print(part.text)                         # the model may comment on the result
