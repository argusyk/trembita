# Appendix A. Laboratory Practicum – example 4 (manuscript: 90-appendix-a.md, line 227)
from trembita.assistant import chat_turn
from trembita.client import make_client

def confirm_in_console(name: str, args: dict) -> bool:
    """A human sees the action and its parameters and decides on their own."""
    print(f"The assistant proposes to run {name} with parameters {args}")
    return input("Confirm? [yes/no] ").strip().lower() == "yes"

history = []
print(chat_turn(make_client(), history, "Book Murchyk the cat in with the GP for tomorrow",
                confirm=confirm_in_console))
