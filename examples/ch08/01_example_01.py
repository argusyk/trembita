# Розділ 8. Інженерія підказок для Gemini – приклад 1 (рукопис: 08-pidkazky.md, рядок 63)
from datetime import date

from google import genai
from google.genai import types

from trembita.prompts import SYSTEM_INSTRUCTION   # підрозділ 8.8

client = genai.Client()


def system_for(today: date) -> str:
    """Стабільна інструкція + дата: префікс змінюється раз на добу."""
    return f"{SYSTEM_INSTRUCTION}\nСьогодні {today:%d.%m.%Y}."


resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Оформи забір 300 кг з нашого складу в Ужгороді на завтра.",
    config=types.GenerateContentConfig(system_instruction=system_for(date.today())),
)
print(resp.text)
