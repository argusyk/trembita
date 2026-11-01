# Appendix D. Code Recipes – example 9 (manuscript: 93-appendix-d.md, line 150)
resp = client.models.generate_content(
    model="gemini-4-argon",
    contents="70 pallets of 420 kg each; a semi-trailer takes 33 pallet places and 24 t. How many trips?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="medium")),
)
um = resp.usage_metadata
print("thoughts:", um.thoughts_token_count, "answer:", um.candidates_token_count)
billed_out = (um.thoughts_token_count or 0) + (um.candidates_token_count or 0)
