# Appendix D. Code Recipes – example 18 (manuscript: 93-appendix-d.md, line 331)
contract = client.files.upload(file="dohovir_perevezennia_2026.pdf")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[contract, "Find the clauses on the carrier's liability, "
                        "give the page and quote the key sentence."],
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM),
)
print(resp.text)
