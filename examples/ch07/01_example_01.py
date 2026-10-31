# Розділ 7. Gemini API і Google Gen AI SDK – приклад 1 (рукопис: 07-api.md, рядок 28)
from google import genai

# Шлях 1: Gemini Developer API. Ключ береться зі змінної GEMINI_API_KEY
# (або GOOGLE_API_KEY, яка має пріоритет, якщо задано обидві).
client = genai.Client()

# Шлях 2: Agent Platform (колишній Vertex AI). Облікові дані – з Application
# Default Credentials: gcloud auth application-default login
cloud_client = genai.Client(
    vertexai=True,                   # у SDK 2.x є й новіша назва: enterprise=True
    project="smereka-trembita",      # ідентифікатор проєкту Google Cloud
    location="europe-west4",         # регіон обробки запитів
)

for c in (client, cloud_client):
    resp = c.models.generate_content(
        model="gemini-3.8-flash",
        contents="Одним реченням: що таке накладна CMR?",
    )
    print(resp.text)
