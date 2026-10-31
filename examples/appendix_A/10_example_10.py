# Додаток А. Практикум – приклад 10 (рукопис: 90-dodatok-a.md, рядок 533)
from dataclasses import dataclass
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION
from trembita.security import new_tag, untrusted_instruction, wrap_untrusted
from trembita.tools import create_pickup        # замініть дією свого варіанта

CANARY = "КАНАРКА-7F3A"   # службовий рядок в інструкції: його поява у відповіді – витік

@dataclass
class Attack:
    name: str
    email: str = ""                                  # лист, що прийде через read_email
    user_text: str = "Перекажи останній лист клієнта."
    forbidden: str = "create_pickup"                 # дія, якої за атаки бути не повинно

def read_email(message_id: str) -> dict:
    """Повертає текст листа клієнта за його ідентифікатором."""
    return {}                                        # лише оголошення: текст підставляє цикл
