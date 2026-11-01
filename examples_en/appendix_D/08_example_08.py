# Appendix D. Code Recipes – example 8 (manuscript: 93-appendix-d.md, line 128)
SYSTEM = "You are Trembita, the assistant of the logistics company Smereka."
GEN = {"max_output_tokens": 1024, "thinking_level": "low"}

first = client.interactions.create(
    model="gemini-3.8-flash", input="How many days does a shipment take from Lviv to Warsaw?",
    system_instruction=SYSTEM, generation_config=GEN)
print(first.status, first.output_text)

follow = client.interactions.create(
    model="gemini-3.8-flash", input="And to Krakow?",
    previous_interaction_id=first.id,        # the server supplies the history
    system_instruction=SYSTEM, generation_config=GEN)
print(follow.output_text, follow.usage.total_output_tokens)
