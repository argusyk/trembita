# Chapter 6. The Gemini Model Family and the Open Gemma Models – example 4 (manuscript: 06-rodyna-modeley.md, line 243)
# The same Gemma 4 through the Gemini API: compare it with 3.8 Flash on one request
question = "Classify the email: 'The pallet arrived with a damaged corner, SM-2610-0117'."
for model in ("gemma-4-31b-it", "gemini-3.8-flash"):
    resp = client.models.generate_content(model=model, contents=question)
    print(model, "|", (resp.text or "").strip()[:120])
