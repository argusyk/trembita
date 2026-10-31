# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 8 (рукопис: 13-optymizatsiya.md, рядок 417)
import datetime as dt
from google import genai
from google.genai import errors, types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION


class RegulationsCache:
    """Явний кеш регламенту «Смереки» лише на робочі години диспетчерської."""

    def __init__(self, client: genai.Client, text: str, shift_end_utc: int = 17):
        self.client, self.text, self.shift_end_utc = client, text, shift_end_utc
        self.name: str | None = None

    def ensure(self) -> str | None:
        now = dt.datetime.now(dt.timezone.utc)
        end = now.replace(hour=self.shift_end_utc, minute=0, second=0, microsecond=0)
        if now >= end:
            return None                       # поза зміною: працює неявне кешування
        if self.name:
            try:
                self.client.caches.get(name=self.name)
                return self.name
            except errors.ClientError:
                self.name = None              # кеш сплив або його видалили
        cache = self.client.caches.create(model=MODEL_MAIN, config=types.CreateCachedContentConfig(
            display_name="reglament-smereka", system_instruction=SYSTEM_INSTRUCTION,
            contents=[types.Content(role="user", parts=[types.Part(text=self.text)])],
            expire_time=end,                  # живе рівно до кінця зміни
        ))
        self.name = cache.name
        return self.name
