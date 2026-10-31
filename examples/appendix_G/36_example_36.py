# Додаток Г. Довідник рецептів коду – приклад 36 (рукопис: 93-dodatok-g.md, рядок 734)
import numpy as np

def embed(texts: list[str], task: str, dim: int = 768) -> np.ndarray:
    resp = client.models.embed_content(
        model="gemini-embedding-2", contents=texts,
        config=types.EmbedContentConfig(task_type=task, output_dimensionality=dim))
    m = np.array([e.values for e in resp.embeddings], dtype=np.float32)
    return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-12)

chunks = ["Вантажі класу ADR 3 приймає лише склад у Львові.",
          "Претензію про пошкодження подають протягом 7 днів."]
matrix = embed(chunks, task="RETRIEVAL_DOCUMENT")

def search(query: str, k: int = 1) -> list[tuple[str, float]]:
    scores = matrix @ embed([query], task="RETRIEVAL_QUERY")[0]
    return [(chunks[i], float(scores[i])) for i in np.argsort(-scores)[:k]]

print(search("Куди везти легкозаймисту рідину?"))
