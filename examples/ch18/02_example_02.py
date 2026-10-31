# Розділ 18. Gemini для знаннєвої роботи: Workspace, NotebookLM, Deep Research і Gemini Enterprise – приклад 2 (рукопис: 18-znannieva-robota.md, рядок 155)
# Спільне планування: спершу план, дослідження – після підтвердження
plan = wait(client.interactions.create(
    agent=DR_AGENT,
    input=TOPIC,
    agent_config={"type": "deep-research", "collaborative_planning": True},
    background=True,
))
print(plan.output_text)              # Марта читає план і вирішує, що змінити

report = wait(client.interactions.create(
    agent=DR_AGENT,
    input="План підходить. Додай порівняння з поромними перевезеннями, Молдову прибери.",
    previous_interaction_id=plan.id,  # продовження тієї самої розмови
    background=True,
))
print(report.output_text[:2000])
