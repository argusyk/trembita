# Розділ 9. Мислення: рівні, бюджети й підписи думок – приклад 4 (рукопис: 09-myslennia.md, рядок 138)
from google import genai

client = genai.Client()
interaction = client.interactions.create(
    model="gemini-4-argon",
    input="Чи вкладеться рейс Київ–Варшава в норми режиму праці водія, якщо виїзд о 6:00?",
    generation_config={"thinking_level": "high", "thinking_summaries": "auto"},
)
for step in interaction.steps or []:
    if step.type == "thought":
        for item in step.summary or []:
            print("[резюме думок]", getattr(item, "text", ""))
print(interaction.output_text)
print("токенів мислення:", interaction.usage.total_thought_tokens)
