# Розділ 19. Безпека застосунків і ризики – приклад 4 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 180)
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN

PROJECT, LOCATION = "smereka-prod", "europe-west1"   # регіон, де створено шаблони
TPL = f"projects/{PROJECT}/locations/{LOCATION}/templates"

client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
armor = types.ModelArmorConfig(
    prompt_template_name=f"{TPL}/trembita-input",     # впровадження, джейлбрейк, URL
    response_template_name=f"{TPL}/trembita-output",  # персональні дані, шкідливий вміст
)

def ask_armored(text: str) -> str:
    resp = client.models.generate_content(
        model=MODEL_MAIN, contents=text,
        config=types.GenerateContentConfig(model_armor_config=armor),
    )
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason == types.BlockedReason.MODEL_ARMOR:
        return "Запит містить ознаки атаки й не буде опрацьований."
    return resp.text or ""
