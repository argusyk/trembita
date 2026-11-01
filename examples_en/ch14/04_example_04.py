# Chapter 14. The Live API and media generation – example 4 (manuscript: 14-live-media.md, line 199)
import datetime as dt
from google import genai
from google.genai import types
from trembita.config import MODEL_LIVE
from trembita.tools import create_pickup, find_warehouse, track_shipment

client = genai.Client(http_options={"api_version": "v1alpha"})   # the real key lives only on the backend
DRIVER_INSTRUCTION = ("You are Trembita, the voice assistant for Smereka's drivers. Answer briefly, "
                      "without lists or markup; say numbers in words.")
DRIVER_LOCKED = types.LiveConnectConfig(                  # what the application cannot change
    response_modalities=["AUDIO"],
    system_instruction=DRIVER_INSTRUCTION,
    tools=[track_shipment, find_warehouse, create_pickup],  # the SDK turns functions into declarations
)


def issue_driver_token(driver_id: str) -> str:
    """After the driver logs in and before every reconnection; the backend verifies driver_id."""
    now = dt.datetime.now(dt.timezone.utc)
    token = client.auth_tokens.create(config=types.CreateAuthTokenConfig(
        uses=1,                                              # one new session per token
        expire_time=now + dt.timedelta(hours=2),             # length of a trip segment
        new_session_expire_time=now + dt.timedelta(minutes=1),
        live_connect_constraints=types.LiveConnectConstraints(model=MODEL_LIVE, config=DRIVER_LOCKED),
        lock_additional_fields=[],                           # lock only the fields set above
    ))
    return token.name                                        # this value goes to the application
