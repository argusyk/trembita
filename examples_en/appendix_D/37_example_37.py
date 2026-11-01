# Appendix D. Code Recipes – example 37 (manuscript: 93-appendix-d.md, line 761)
H, T = types.HarmCategory, types.HarmBlockThreshold
config = types.GenerateContentConfig(safety_settings=[
    types.SafetySetting(category=H.HARM_CATEGORY_HARASSMENT, threshold=T.BLOCK_MEDIUM_AND_ABOVE),
    types.SafetySetting(category=H.HARM_CATEGORY_HATE_SPEECH, threshold=T.BLOCK_MEDIUM_AND_ABOVE),
    # ADR classes and flammable cargo are a working topic for dispatchers
    types.SafetySetting(category=H.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=T.BLOCK_ONLY_HIGH),
])
