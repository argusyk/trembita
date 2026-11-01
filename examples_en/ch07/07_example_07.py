# Chapter 7. The Gemini API and the Google Gen AI SDK – example 7 (manuscript: 07-api.md, line 316)
from google import genai

client = genai.Client()
SYSTEM = "You are Trembita, the assistant of the logistics company Smereka."
GEN = {"max_output_tokens": 1024, "thinking_level": "low"}

first = client.interactions.create(
    model="gemini-3.8-flash",
    input="How many days does cargo take from Lviv to Warsaw?",
    system_instruction=SYSTEM,
    generation_config=GEN,
)
print(first.status, first.output_text)

# Next step: the server keeps the history, but we pass the instruction and settings again
follow = client.interactions.create(
    model="gemini-3.8-flash",
    input="And to Krakow?",
    previous_interaction_id=first.id,
    system_instruction=SYSTEM,
    generation_config=GEN,
)
print(follow.output_text)
print("tokens:", follow.usage.total_input_tokens, follow.usage.total_output_tokens)
