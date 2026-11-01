# Chapter 8. Prompt Engineering for Gemini – example 1 (manuscript: 08-pidkazky.md, line 63)
from datetime import date

from google import genai
from google.genai import types

from trembita.prompts import SYSTEM_INSTRUCTION   # Section 8.8

client = genai.Client()


def system_for(today: date) -> str:
    """Stable instruction + date: the prefix changes once a day."""
    return f"{SYSTEM_INSTRUCTION}\nToday is {today:%d.%m.%Y}."


resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Book a pickup of 300 kg from our warehouse in Uzhhorod for tomorrow.",
    config=types.GenerateContentConfig(system_instruction=system_for(date.today())),
)
print(resp.text)
