# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 3 (рукопис: 21-rag.md, рядок 178)
class VectorIndex:
    """Точний пошук у пам'яті: годиться до сотень тисяч фрагментів."""

    def __init__(self, chunks: list[dict], dim: int = 768, batch: int = 100):
        self.chunks, self.dim = chunks, dim
        parts = [embed([c["text"] for c in chunks[i:i + batch]],
                       task="RETRIEVAL_DOCUMENT", dim=dim)
                 for i in range(0, len(chunks), batch)]   # розмір пакета – за лімітами API
        self.matrix = np.vstack(parts)                    # (N, dim), рядки нормовані

    def search(self, query: str, k: int = 5) -> list[int]:
        """Повертає індекси k найближчих фрагментів, найкращий першим."""
        q = embed([query], task="RETRIEVAL_QUERY", dim=self.dim)[0]
        scores = self.matrix @ q                          # косинус = скалярний добуток
        k = min(k, len(scores))
        top = np.argpartition(-scores, k - 1)[:k]         # k кращих без повного сортування
        return [int(i) for i in top[np.argsort(-scores[top])]]
