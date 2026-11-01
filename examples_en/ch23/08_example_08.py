# Chapter 23. Production on Gemini Enterprise Agent Platform – example 8 (manuscript: 23-produkshn.md, line 416)
from google.genai import types

# Before (Gemini 2.5 Flash, retired 20.10.2026):
old_config = types.GenerateContentConfig(
    temperature=0.2,
    thinking_config=types.ThinkingConfig(thinking_budget=1024),
)

# After (Gemini 3.8 Flash or 4 Argon):
new_config = types.GenerateContentConfig(
    # temperature is not set: the default 1.0 is recommended for Gemini 3+
    thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
)


def warn_if_retiring(resp) -> None:
    """Prints a warning if the server reported an outdated model."""
    st = resp.model_status
    if st and st.model_stage in (types.ModelStage.LEGACY, types.ModelStage.DEPRECATED):
        print(f"Warning: {resp.model_version} – {st.model_stage}, retirement {st.retirement_time}")
