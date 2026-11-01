# Appendix A. Laboratory Practicum – example 1 (manuscript: 90-appendix-a.md, line 94)
from google import genai
from trembita.costs import cost_from_usage

client = genai.Client()  # the key is in the GEMINI_API_KEY environment variable
SAMPLES = {
    "sentence": "Is ibuprofen 400 mg in stock?",
    "para uk": open("ua.txt", encoding="utf-8").read(),
    "para en": open("en.txt", encoding="utf-8").read(),
}
for name, text in SAMPLES.items():
    n = client.models.count_tokens(model="gemini-3.8-flash", contents=text).total_tokens
    print(f"{name:10} {len(text):6} chars {n:6} tok. {len(text) / n:5.2f}")

resp = client.models.generate_content(model="gemini-3.8-flash", contents=SAMPLES["sentence"])
um = resp.usage_metadata
print("Flash, USD:", cost_from_usage("gemini-3.8-flash", um))   # thoughts and cache are included
print("Argon, USD:", cost_from_usage("gemini-4-argon", um))     # the same tokens at Argon prices
