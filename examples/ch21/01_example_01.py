# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 1 (рукопис: 21-rag.md, рядок 71)
import numpy as np
from google import genai
from google.genai import types

client = genai.Client()
MODEL_EMBED = "gemini-embedding-2"


def embed(texts: list[str], task: str, dim: int = 768) -> np.ndarray:
    """Повертає матрицю (len(texts), dim) з рядками одиничної довжини."""
    resp = client.models.embed_content(
        model=MODEL_EMBED,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task,              # RETRIEVAL_DOCUMENT або RETRIEVAL_QUERY
            output_dimensionality=dim,   # без параметра – 3072 виміри
        ),
    )
    m = np.array([e.values for e in resp.embeddings], dtype=np.float32)
    # обрізаний вектор уже не має довжини 1 – нормуємо заново
    return m / np.linalg.norm(m, axis=1, keepdims=True)


docs = embed(["Вантажі класу ADR 3 приймає лише склад у Львові.",
              "Претензію про пошкодження подають протягом 7 днів."],
             task="RETRIEVAL_DOCUMENT")
q = embed(["Куди везти легкозаймисту рідину?"], task="RETRIEVAL_QUERY")
print(docs @ q[0])          # косинусна подібність до кожного фрагмента
