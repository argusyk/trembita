# Розділ 19. Безпека застосунків і ризики – приклад 2 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 122)
from google.genai import types

# Пороги «Трембіти»: суворо до образ, поблажливіше до тем небезпечних вантажів
SAFETY = [
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
    # ADR-класи, вибухові й легкозаймисті вантажі – робоча тема диспетчерів
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH),
]

config = types.GenerateContentConfig(safety_settings=SAFETY)
