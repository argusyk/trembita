# Chapter 3. Tokens, Multimodal Tokens and Long Context – example 4 (manuscript: 03-tokeny-kontekst.md, line 246)
from google import genai
from google.genai import types

client = genai.Client()

# the Files API keeps files for 48 h: in repeated runs fetch them with
# client.files.get(name=...) instead of uploading them anew each time
paths = ["reglament_perevezen.pdf"] + [f"dogovory/d{i:02d}.pdf" for i in range(1, 41)]
files = [client.files.upload(file=p) for p in paths]

parts = []
for path, f in zip(paths, files):
    parts += [types.Part(text=f"<document: {path}>"), f]   # a label before each document

question = (
    "Claim SM-2610-0388: the cargo arrived in Uzhhorod three days late. "
    "Which clauses of the regulations and of the contract with the carrier apply? "
    "First quote these clauses verbatim with the document name, then give a conclusion."
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[*parts, question],        # the question goes last, after the documents
    config=types.GenerateContentConfig(
        system_instruction="You are a legal assistant in Smereka's claims department.",
        max_output_tokens=16384,        # with room for thinking and the response
    ),
)
print(resp.text)
u = resp.usage_metadata
print(u.prompt_token_count, u.thoughts_token_count, u.candidates_token_count)
