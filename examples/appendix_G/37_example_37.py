# Додаток Г. Довідник рецептів коду – приклад 37 (рукопис: 93-dodatok-g.md, рядок 761)
H, T = types.HarmCategory, types.HarmBlockThreshold
config = types.GenerateContentConfig(safety_settings=[
    types.SafetySetting(category=H.HARM_CATEGORY_HARASSMENT, threshold=T.BLOCK_MEDIUM_AND_ABOVE),
    types.SafetySetting(category=H.HARM_CATEGORY_HATE_SPEECH, threshold=T.BLOCK_MEDIUM_AND_ABOVE),
    # ADR-класи й легкозаймисті вантажі – робоча тема диспетчерів
    types.SafetySetting(category=H.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=T.BLOCK_ONLY_HIGH),
])
