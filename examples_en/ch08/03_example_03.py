# Chapter 8. Prompt Engineering for Gemini – example 3 (manuscript: 08-pidkazky.md, line 168)
from google import genai
from google.genai import types

client = genai.Client()
contract = open("contract_smereka_counterparty.txt", encoding="utf-8").read()

prompt = f"""<contract>
{contract}
</contract>

<facts>
Cargo accepted on 03.10.2026, delivered on 09.10.2026. Route Lviv - Wroclaw.
</facts>

Relying only on the <contract> and <facts> above, answer:
1. Quote verbatim the contract clauses on delivery deadlines.
2. Determine whether the deadline was breached. If the contract gives no unambiguous answer, say so.
Format: quotes first, then the conclusion in one sentence."""

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction="You are the legal assistant of Smereka's claims department.",
    ),
)
print(resp.text)
