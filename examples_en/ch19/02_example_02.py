# Chapter 19. Application Security and Risks – example 2 (manuscript: 19-bezpeka-zastosunkiv.md, line 164)
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN

PROJECT, LOCATION = "smereka-prod", "europe-west1"   # region where the templates were created
TPL = f"projects/{PROJECT}/locations/{LOCATION}/templates"

client = make_client(vertexai=True, project=PROJECT, location=LOCATION)  # Agent Platform
armor = types.ModelArmorConfig(
    prompt_template_name=f"{TPL}/trembita-input",     # injection, jailbreak, URLs
    response_template_name=f"{TPL}/trembita-output",  # personal data, harmful content
)

def ask_armored(text: str) -> str:
    resp = client.models.generate_content(
        model=MODEL_MAIN, contents=text,
        config=types.GenerateContentConfig(model_armor_config=armor),
    )
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason == types.BlockedReason.MODEL_ARMOR:
        return "The request shows signs of an attack and will not be processed."
    return resp.text or ""
