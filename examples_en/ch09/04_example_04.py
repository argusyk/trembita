# Chapter 9. Thinking: Levels, Budgets and Thought Signatures – example 4 (manuscript: 09-myslennia.md, line 138)
from google import genai

client = genai.Client()
interaction = client.interactions.create(
    model="gemini-4-argon",
    input="Will a Kyiv–Warsaw trip fit within the driver's working-time rules if departure is at 6:00?",
    generation_config={"thinking_level": "high", "thinking_summaries": "auto"},
)
for step in interaction.steps or []:
    if step.type == "thought":
        for item in step.summary or []:
            print("[thought summary]", getattr(item, "text", ""))
print(interaction.output_text)
print("thinking tokens:", interaction.usage.total_thought_tokens)
