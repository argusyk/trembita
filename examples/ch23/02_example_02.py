# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 2 (рукопис: 23-produkshn.md, рядок 97)
import os
from trembita.client import make_client

client = make_client(
    vertexai=True,           # у SDK 2.x той самий прапорець зветься enterprise=True
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4"),
)
