# Додаток Г. Довідник рецептів коду – приклад 35 (рукопис: 93-dodatok-g.md, рядок 710)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH, RemoteA2aAgent

# 1) окремий агент лише для читання; запуск за проксі з автентифікацією:
#    uvicorn server_tracker:app (до uvicorn ззовні не дістатися)
app = to_a2a(agent, host="agents.smereka.example", port=443, protocol="https")

# 2) агент партнера як субагент
dunai_cargo = RemoteA2aAgent(
    name="dunai_cargo",
    description="Агент перевізника «Дунай-Карго»: рейси до ЄС, бронювання місць.",
    agent_card=f"https://agents.dunai-cargo.example{AGENT_CARD_WELL_KNOWN_PATH}")
customs_agent = Agent(name="customs", model="gemini-3.8-flash",
                      instruction="Про рейси й місця питай dunai_cargo.",
                      sub_agents=[dunai_cargo])
