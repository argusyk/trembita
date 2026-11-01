# Chapter 15. Agents on Gemini: the Agent Development Kit and the A2A protocol – example 2 (manuscript: 15-ahenty-adk.md, line 128)
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
    msg = types.Content(role="user", parts=[types.Part(text="Where is SM-2610-0042 now?")])
    async for event in runner.run_async(
        user_id="iryna", session_id=session.id, new_message=msg
    ):
        for call in event.get_function_calls():
            print("action:", call.name, call.args)          # the "action" step of (15.1)
        if event.is_final_response() and event.content:
            print("answer:", event.content.parts[0].text)


asyncio.run(main())
