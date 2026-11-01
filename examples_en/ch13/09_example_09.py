# Chapter 13. Optimization: context caching, batch processing and cost – example 9 (manuscript: 13-optymizatsiya.md, line 446)
import datetime as dt
from zoneinfo import ZoneInfo
from google import genai
from google.genai import errors, types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

KYIV = ZoneInfo("Europe/Kyiv")                # the shift follows Kyiv time, including daylight saving


class RegulationsCache:
    """Explicit cache of Smereka's regulations, only during the dispatch office's working hours."""

    def __init__(self, client: genai.Client, text: str,
                 shift_start: dt.time = dt.time(8), shift_end: dt.time = dt.time(19)):
        self.client, self.text = client, text
        self.shift_start, self.shift_end = shift_start, shift_end
        self.name: str | None = None

    def ensure(self) -> str | None:
        now = dt.datetime.now(KYIV)
        start = dt.datetime.combine(now.date(), self.shift_start, tzinfo=KYIV)
        end = dt.datetime.combine(now.date(), self.shift_end, tzinfo=KYIV)
        if not start <= now < end:
            return None                       # outside the shift: implicit caching does the work
        if self.name:
            try:
                self.client.caches.get(name=self.name)
                return self.name
            except errors.ClientError as e:
                if e.code != 404:
                    raise                     # 429, 403 etc.: a new cache will not help here
                self.name = None              # 404: the cache has expired or been deleted
        cache = self.client.caches.create(model=MODEL_MAIN, config=types.CreateCachedContentConfig(
            display_name="reglament-smereka", system_instruction=SYSTEM_INSTRUCTION,
            contents=[types.Content(role="user", parts=[types.Part(text=self.text)])],
            expire_time=end.astimezone(dt.timezone.utc),   # lives exactly until the end of the shift
        ))
        self.name = cache.name
        return self.name
