# Appendix D. Code Recipes – example 36 (manuscript: 93-appendix-d.md, line 734)
import numpy as np

def embed(texts: list[str], task: str, dim: int = 768) -> np.ndarray:
    resp = client.models.embed_content(
        model="gemini-embedding-2", contents=texts,
        config=types.EmbedContentConfig(task_type=task, output_dimensionality=dim))
    m = np.array([e.values for e in resp.embeddings], dtype=np.float32)
    return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-12)

chunks = ["ADR class 3 cargo is accepted only by the warehouse in Lviv.",
          "A damage claim is filed within 7 days."]
matrix = embed(chunks, task="RETRIEVAL_DOCUMENT")

def search(query: str, k: int = 1) -> list[tuple[str, float]]:
    scores = matrix @ embed([query], task="RETRIEVAL_QUERY")[0]
    return [(chunks[i], float(scores[i])) for i in np.argsort(-scores)[:k]]

print(search("Where should a flammable liquid be taken?"))
