"""Планування доставки з Картами, Пошуком і виконанням коду (розділ 12).

Три етапи (пункти пропуску, новини про кордон, розрахункова вага) одне від одного не залежать:
plan_delivery() виконує їх по черзі, plan_delivery_async() – одночасно (asyncio.gather).
Від них залежить лише тариф, який рахує наша функція get_tariff. Розбір відповідей винесено
в чисті функції (response_text, code_outputs, parse_result_line, web_sources).
"""
import asyncio
import re
from datetime import datetime, timedelta, timezone

from google.genai import types

from .config import MODEL_MAIN
from .tools import get_tariff

_NUMBER = re.compile(r"[-+]?\d+(?:[.,]\d+)?")


def response_text(resp) -> str:
    """resp.text або порожній рядок (блок, порожня відповідь)."""
    try:
        return resp.text or ""
    except (AttributeError, ValueError):
        return ""


def _parts(resp) -> list:
    cands = getattr(resp, "candidates", None) or []
    content = getattr(cands[0], "content", None) if cands else None
    return list(getattr(content, "parts", None) or [])


def code_outputs(resp) -> list[str]:
    """Виводи вдалих запусків коду (outcome OK) у порядку виконання."""
    return [p.code_execution_result.output or "" for p in _parts(resp)
            if getattr(p, "code_execution_result", None)
            and p.code_execution_result.outcome == types.Outcome.OUTCOME_OK]


def parse_result_line(output: str) -> tuple[float, float] | None:
    """(вага_кг, об'єм_м3) з останнього рядка «RESULT <вага> <об'єм>» або None.

    Розуміє десяткову кому й одиниці: «RESULT 2500,0 7,2», «RESULT 2500 кг 7.2 м3».
    """
    lines = [ln.strip() for ln in str(output).splitlines() if ln.strip().upper().startswith("RESULT")]
    if not lines:
        return None
    nums = _NUMBER.findall(lines[-1][len("RESULT"):].replace("м3", " ").replace("м³", " "))
    if len(nums) < 2:
        return None
    kg, m3 = (float(n.replace(",", ".")) for n in nums[:2])
    if kg <= 0 or m3 < 0:
        return None
    return kg, m3


def web_sources(resp) -> list[dict]:
    """Джерела пошуку з grounding_metadata (порожньо, якщо модель не шукала)."""
    cands = getattr(resp, "candidates", None) or []
    meta = getattr(cands[0], "grounding_metadata", None) if cands else None
    out = []
    for c in (getattr(meta, "grounding_chunks", None) or []):
        web = getattr(c, "web", None)
        if web is not None and web.uri:
            out.append({"uri": web.uri, "title": web.title or "", "domain": web.domain or ""})
    return out


def _prompts(origin: str, destination: str, cargo_text: str, now: datetime):
    return [
        (f"Які вантажні пункти пропуску Україна – Польща найзручніші для маршруту "
         f"{origin} – {destination}? Для кожного: де стоянка.",
         types.Tool(google_maps=types.GoogleMaps())),
        ("Стан черг і обмеження для вантажівок на пунктах пропуску Україна – Польща. "
         "Лише факти з датами.",
         types.Tool(google_search=types.GoogleSearch(
             time_range_filter=types.Interval(start_time=now - timedelta(days=3), end_time=now)))),
        (cargo_text + " Порахуй кодом об'єм, фактичну й розрахункову вагу (1 м³ = 250 кг). "
         "Останнім рядком виведи рівно: RESULT <вага_кг> <об'єм_м3> (числа з крапкою, без одиниць)",
         types.Tool(code_execution=types.ToolCodeExecution())),
    ]


def _assemble(origin: str, destination: str, places, news, weight) -> dict:
    runs = code_outputs(weight)
    parsed = parse_result_line(runs[-1]) if runs else None      # остання вдала спроба
    kg, m3 = parsed or (None, None)
    return {
        "crossings": response_text(places), "border_news": response_text(news),
        "sources": web_sources(news),
        "billable_kg": kg, "volume_m3": m3,
        "tariff": get_tariff(origin, destination, kg, m3) if kg else None,
        "issues": [] if parsed else ["Не вдалося обчислити вагу – уточніть опис вантажу"],
        "status": "draft"}               # план – чернетка; рішення ухвалює диспетчер


def plan_delivery(origin: str, destination: str, cargo_text: str, *, client=None,
                  model: str = MODEL_MAIN, now: datetime | None = None) -> dict:
    """Чернетка плану доставки; етапи по черзі."""
    from .client import make_client
    client = client or make_client()
    now = now or datetime.now(timezone.utc)
    resps = [client.models.generate_content(model=model, contents=prompt,
                                            config=types.GenerateContentConfig(tools=[tool]))
             for prompt, tool in _prompts(origin, destination, cargo_text, now)]
    return _assemble(origin, destination, *resps)


async def plan_delivery_async(origin: str, destination: str, cargo_text: str, *, client=None,
                              model: str = MODEL_MAIN, now: datetime | None = None) -> dict:
    """Те саме, але три незалежні етапи йдуть одночасно: затримка ≈ найдовшого етапу."""
    from .client import make_client
    client = client or make_client()
    now = now or datetime.now(timezone.utc)
    resps = await asyncio.gather(*[
        client.aio.models.generate_content(model=model, contents=prompt,
                                           config=types.GenerateContentConfig(tools=[tool]))
        for prompt, tool in _prompts(origin, destination, cargo_text, now)])
    return _assemble(origin, destination, *resps)
