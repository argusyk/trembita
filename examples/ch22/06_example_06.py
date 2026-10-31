# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 6 (рукопис: 22-computer-use.md, рядок 307)
def ask_human(action: str, args: dict, why: str) -> bool:
    """Показує дію брокерові; без явного «так» дія не виконується."""
    print(f"Агент хоче виконати: {action} {args}\nЧому потрібне підтвердження: {why}")
    return input("Дозволити? [так/ні] ").strip().lower() == "так"


strict_tool = types.Tool(computer_use=types.ComputerUse(
    environment=types.Environment.ENVIRONMENT_BROWSER,
    excluded_predefined_functions=UNSUPPORTED,   # з підрозділу 22.3, разом із search
    enable_prompt_injection_detection=True,      # перевіряти екран на впровадження
))
