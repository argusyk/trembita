# Додаток А. Практикум – приклад 4 (рукопис: 90-dodatok-a.md, рядок 207)
from trembita.assistant import chat_turn
from trembita.client import make_client

def confirm_in_console(name: str, args: dict) -> bool:
    """Людина бачить дію й параметри та вирішує сама."""
    print(f"Асистент пропонує виконати {name} з параметрами {args}")
    return input("Підтвердити? [так/ні] ").strip().lower() == "так"

history = []
print(chat_turn(make_client(), history, "Запишіть кота Мурчика на завтра до терапевта",
                confirm=confirm_in_console))
