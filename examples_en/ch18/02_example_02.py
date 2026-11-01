# Chapter 18. Gemini for Knowledge Work: Workspace, NotebookLM, Deep Research and Gemini Enterprise – example 2 (manuscript: 18-znannieva-robota.md, line 157)
# Collaborative planning: plan first, research after confirmation
plan = wait(client.interactions.create(
    agent=DR_AGENT,
    input=TOPIC,
    agent_config={"type": "deep-research", "collaborative_planning": True},
    background=True,
))
print(plan.output_text)              # Marta reads the plan and decides what to change

report = wait(client.interactions.create(
    agent=DR_AGENT,
    input="The plan is fine. Add a comparison with ferry transport, remove Moldova.",
    previous_interaction_id=plan.id,  # continuation of the same conversation
    background=True,
))
print((report.output_text or "")[:2000])
