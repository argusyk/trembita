# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 9 (рукопис: 13-optymizatsiya.md, рядок 446)
import datetime as dt
from zoneinfo import ZoneInfo
from google import genai
from google.genai import errors, types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

KYIV = ZoneInfo("Europe/Kyiv")                # зміна – за київським часом, з переходом на літній


class RegulationsCache:
    """Явний кеш регламенту «Смереки» лише на робочі години диспетчерської."""

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
            return None                       # поза зміною: працює неявне кешування
        if self.name:
            try:
                self.client.caches.get(name=self.name)
                return self.name
            except errors.ClientError as e:
                if e.code != 404:
                    raise                     # 429, 403 тощо: новий кеш тут не допоможе
                self.name = None              # 404: кеш сплив або його видалили
        cache = self.client.caches.create(model=MODEL_MAIN, config=types.CreateCachedContentConfig(
            display_name="reglament-smereka", system_instruction=SYSTEM_INSTRUCTION,
            contents=[types.Content(role="user", parts=[types.Part(text=self.text)])],
            expire_time=end.astimezone(dt.timezone.utc),   # живе рівно до кінця зміни
        ))
        self.name = cache.name
        return self.name
