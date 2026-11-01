# Chapter 1. What Is Gemini: Google DeepMind, the Ecosystem and a Running Example – example 3 (manuscript: 01-vstup-gemini.md, line 259)
from google import genai

client = genai.Client()  # the key is taken from the GEMINI_API_KEY variable
first = client.interactions.create(
    model="gemini-3.8-flash",
    input="What documents are needed to transport cargo to Poland?",
)
print(first.output_text)

# continuing the conversation: the server fills in the history itself
follow = client.interactions.create(
    model="gemini-3.8-flash",
    input="And what if the cargo is dangerous?",
    previous_interaction_id=first.id,
)
print(follow.output_text)
