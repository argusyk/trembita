# Розділ 9. Мислення: рівні, бюджети й підписи думок – приклад 6 (рукопис: 09-myslennia.md, рядок 216)
from google.genai import types

PRICES = {"gemini-4-argon": (2.00, 10.00),     # дол. за 1 млн: вхід, вихід (жовтень 2026)
          "gemini-3.8-flash": (0.75, 3.75)}    # орієнтовно, звіряйте з прайсом

def request_cost(model: str, resp: types.GenerateContentResponse) -> dict:
    """Повертає токени та вартість запиту згідно з формулою (9.1)."""
    um = resp.usage_metadata
    p_in, p_out = PRICES[model]
    n_in = um.prompt_token_count or 0
    n_think = um.thoughts_token_count or 0
    n_out = um.candidates_token_count or 0
    cost = (n_in * p_in + (n_think + n_out) * p_out) / 1_000_000
    return {"вхід": n_in, "думки": n_think, "відповідь": n_out,
            "частка_думок": round(n_think / max(n_think + n_out, 1), 2),
            "вартість_дол": round(cost, 5)}
