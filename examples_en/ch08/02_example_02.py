# Chapter 8. Prompt Engineering for Gemini – example 2 (manuscript: 08-pidkazky.md, line 105)
from google import genai
from google.genai import types

client = genai.Client()

LABELS = ("damage", "delay", "shortage", "documents", "other")
FEW_SHOT = """Determine the claim category: damage, delay, shortage, documents, other.

Claim: The pallet of tiles arrived with a broken corner, 6 packs are cracked.
Category: damage

Claim: the CMR shows the wrong gross weight, customs won't let it through
Category: documents

Claim: The driver was rude to our storekeeper.
Category: other

Claim: We ordered delivery for 12.10, received it on 15.10 without warning.
Category: delay

Claim: The waybill says 40 boxes, we received 37.
Category: shortage
"""


def classify(text: str) -> str:
    resp = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"{FEW_SHOT}\nClaim: {text}\nCategory:",
        config=types.GenerateContentConfig(
            # the model thinks: thoughts also spend max_output_tokens (Chapter 7), so leave headroom
            thinking_config=types.ThinkingConfig(thinking_level="low"),
            max_output_tokens=256,
        ),
    )
    answer = (resp.text or "").strip().lower().rstrip(".")
    return answer if answer in LABELS else "other"    # an answer outside the label set is "other"


print(classify("The driver refused to wait for unloading, the goods were taken back."))
