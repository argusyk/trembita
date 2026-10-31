# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 4 (рукопис: 21-rag.md, рядок 222)
import math
from collections import Counter


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w-]+", text.lower())   # SM-2610-0042 – один терм


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.2, b: float = 0.75):
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lens = np.array([sum(d.values()) for d in self.docs], dtype=float)
        self.k1, self.b, n = k1, b, len(self.docs)
        df = Counter(term for d in self.docs for term in d)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.norm = k1 * (1 - b + b * self.lens / self.lens.mean())

    def rank(self, query: str, k: int = 20) -> list[int]:
        s = np.zeros(len(self.docs))
        for term in set(tokenize(query)):
            if term in self.idf:
                tf = np.array([d[term] for d in self.docs], dtype=float)
                s += self.idf[term] * tf * (self.k1 + 1) / (tf + self.norm)
        return [int(i) for i in np.argsort(-s)[:k] if s[i] > 0]


def rrf(rankings: list[list[int]], k: int = 60) -> list[int]:
    """Злиття рангів; кожен список – індекси фрагментів, найкращий першим."""
    fused = Counter()
    for ranking in rankings:
        for rank, idx in enumerate(ranking, start=1):
            fused[idx] += 1 / (k + rank)
    return [idx for idx, _ in fused.most_common()]


def hybrid_search(query, vindex, bm25, k=6):
    return rrf([vindex.search(query, k=20), bm25.rank(query, k=20)])[:k]
