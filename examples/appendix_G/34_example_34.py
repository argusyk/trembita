# Додаток Г. Довідник рецептів коду – приклад 34 (рукопис: 93-dodatok-g.md, рядок 668)
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

agent = Agent(name="tracker", model="gemini-3.8-flash",
              instruction="Статус бери лише з track_shipment. Клієнт: {user:client_name?}",
              tools=[track_shipment], output_key="tracking_summary")

async def main() -> None:
    sessions = InMemorySessionService()
    runner = Runner(app_name="trembita", agent=agent, session_service=sessions)
    session = await sessions.create_session(app_name="trembita", user_id="iryna",
                                            state={"user:client_name": "Wiener Feinkost"})
    msg = types.Content(role="user", parts=[types.Part(text="Де зараз SM-2610-0042?")])
    async for event in runner.run_async(user_id="iryna", session_id=session.id, new_message=msg):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)

asyncio.run(main())
