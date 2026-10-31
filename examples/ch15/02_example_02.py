# Розділ 15. Агенти на Gemini: Agent Development Kit і протокол A2A – приклад 2 (рукопис: 15-ahenty-adk.md, рядок 128)
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from trembita.agents.tracker import tracker_agent

APP = "trembita"


async def main() -> None:
    sessions = InMemorySessionService()
    runner = Runner(app_name=APP, agent=tracker_agent, session_service=sessions)
    session = await sessions.create_session(
        app_name=APP, user_id="iryna", state={"user:client_name": "Wiener Feinkost"}
    )
    msg = types.Content(role="user", parts=[types.Part(text="Де зараз SM-2610-0042?")])
    async for event in runner.run_async(
        user_id="iryna", session_id=session.id, new_message=msg
    ):
        for call in event.get_function_calls():
            print("дія:", call.name, call.args)          # крок «дія» з (15.1)
        if event.is_final_response() and event.content:
            print("відповідь:", event.content.parts[0].text)


asyncio.run(main())
