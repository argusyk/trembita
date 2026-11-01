# Appendix D. Code Recipes – example 2 (manuscript: 93-appendix-d.md, line 20)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="How much will it cost to deliver 20 kg from Lviv to Kyiv?",
    config=types.GenerateContentConfig(
        system_instruction="You are Trembita, the assistant of the logistics company Smereka.",
        max_output_tokens=2048,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
print(resp.text)
