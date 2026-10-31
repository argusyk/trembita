# Додаток А. Практикум – приклад 1 (рукопис: 90-dodatok-a.md, рядок 74)
from google import genai
from trembita.costs import cost_from_usage, request_cost

client = genai.Client()  # ключ – у змінній середовища GEMINI_API_KEY
SAMPLES = {
    "речення": "Чи є в наявності ібупрофен 400 мг?",
    "абзац uk": open("ua.txt", encoding="utf-8").read(),
    "абзац en": open("en.txt", encoding="utf-8").read(),
}
for name, text in SAMPLES.items():
    n = client.models.count_tokens(model="gemini-3.8-flash", contents=text).total_tokens
    print(f"{name:10} {len(text):6} симв. {n:6} ток. {len(text) / n:5.2f}")

resp = client.models.generate_content(model="gemini-3.8-flash", contents=SAMPLES["речення"])
um = resp.usage_metadata
print("Flash, дол.:", cost_from_usage("gemini-3.8-flash", um))
print("Argon, дол.:", request_cost("gemini-4-argon", um.prompt_token_count, um.candidates_token_count))
