# Chapter 7. The Gemini API and the Google Gen AI SDK – example 1 (manuscript: 07-api.md, line 28)
from google import genai

# Path 1: Gemini Developer API. The key is taken from the GEMINI_API_KEY variable
# (or GOOGLE_API_KEY, which takes priority if both are set).
client = genai.Client()

# Path 2: Agent Platform (formerly Vertex AI). Credentials come from Application
# Default Credentials: gcloud auth application-default login
cloud_client = genai.Client(
    vertexai=True,                   # SDK 2.x also has a newer name: enterprise=True
    project="smereka-trembita",      # Google Cloud project ID
    location="europe-west4",         # region where requests are processed
)

for c in (client, cloud_client):
    resp = c.models.generate_content(
        model="gemini-3.8-flash",
        contents="In one sentence: what is a CMR consignment note?",
    )
    print(resp.text)
