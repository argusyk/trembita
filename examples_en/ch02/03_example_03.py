# Chapter 2. Architecture: the Transformer, Mixture of Experts and Multimodality – example 3 (manuscript: 02-arkhitektura.md, line 406)
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Continue the phrase with one word: Cargo SM-2609-0315 has arrived at",
    config=types.GenerateContentConfig(
        temperature=1.0,         # for Gemini 3+ it is recommended to keep 1.0
        top_p=0.95,              # nucleus sampling
        top_k=40,                # cutting off the tail
        seed=42,                 # reproducibility, to the extent the service supports it
        response_logprobs=True,  # return log probabilities
        logprobs=5,              # the five best candidates at each step
    ),
)
lp = response.candidates[0].logprobs_result
if lp and lp.top_candidates:     # not all models return logprobs
    for cand in lp.top_candidates[0].candidates:
        print(cand.token, round(cand.log_probability, 3))
