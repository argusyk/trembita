# Chapter 23. Production on Gemini Enterprise Agent Platform – example 2 (manuscript: 23-produkshn.md, line 97)
import os
from trembita.client import make_client

client = make_client(
    vertexai=True,           # in SDK 2.x the same flag is called enterprise=True
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4"),
)
