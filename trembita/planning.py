"""Планування доставки з Картами, Пошуком і виконанням коду (розділ 12)."""
from datetime import datetime, timedelta, timezone
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN
from trembita.tools import get_tariff

def _ask(client, prompt: str, tool: types.Tool, **cfg) -> types.GenerateContentResponse:
    return client.models.generate_content(
        model=MODEL_MAIN, contents=prompt,
        config=types.GenerateContentConfig(tools=[tool], **cfg))

def plan_delivery(origin: str, destination: str, cargo_text: str) -> dict:
    client = make_client()
    now = datetime.now(timezone.utc)
    # 1. Maps: пункти пропуску й стоянки на шляху
    places = _ask(client, f"Які вантажні пункти пропуску Україна – Польща найзручніші "
                  f"для маршруту {origin} – {destination}? Для кожного: де стоянка.",
                  types.Tool(google_maps=types.GoogleMaps()))
    # 2. Пошук: новини про стан кордону лише за останні 3 доби
    news = _ask(client, "Стан черг і обмеження для вантажівок на пунктах пропуску "
                "Україна – Польща. Лише факти з датами.",
                types.Tool(google_search=types.GoogleSearch(
                    time_range_filter=types.Interval(start_time=now - timedelta(days=3),
                                                     end_time=now))))
    # 3. Код: розрахункова вага з вільного опису вантажу
    weight = _ask(client, cargo_text + " Порахуй кодом V, фактичну й розрахункову вагу "
                  "(1 м³ = 250 кг). Останнім рядком виведи: RESULT <вага_кг> <об'єм_м3>",
                  types.Tool(code_execution=types.ToolCodeExecution()))
    runs = [p.code_execution_result.output for p in weight.candidates[0].content.parts
            if p.code_execution_result
            and p.code_execution_result.outcome == types.Outcome.OUTCOME_OK]
    last = (runs[-1] if runs else "").strip().splitlines()   # остання вдала спроба
    kg, m3 = map(float, last[-1].split()[1:3]) if last and last[-1].startswith("RESULT") else (0.0, 0.0)
    return {
        "crossings": places.text, "border_news": news.text,
        "sources": [c.web.uri for c in (news.candidates[0].grounding_metadata.grounding_chunks or []) if c.web],
        "billable_kg": kg, "volume_m3": m3,
        "tariff": get_tariff(origin, destination, kg, m3) if kg else None,
        "status": "draft"}               # план – чернетка; рішення ухвалює диспетчер
