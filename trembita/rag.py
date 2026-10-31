"""Мінімальний RAG «Трембіти» (розділ 21): фрагменти, косинусна подібність, гібридний пошук і RRF."""
import math
import re
from collections import Counter

import numpy as np

from .config import MODEL_EMBED


def chunk(text: str, size: int = 800, overlap: int = 150) -> list[str]:
    """Ріже текст на фрагменти по межах абзаців, з перекриттям у символах."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, cur = [], ""
    for p in paras:
        if cur and len(cur) + len(p) + 1 > size:
            out.append(cur)
            cur = cur[-overlap:] + " " + p if overlap else p
        else:
            cur = f"{cur} {p}".strip()
    if cur:
        out.append(cur)
    return out


def cosine_top_k(query_vec, doc_vecs, k: int = 3) -> list[int]:
    """Індекси k найближчих векторів за косинусною подібністю."""
    q = np.asarray(query_vec, dtype=float)
    d = np.asarray(doc_vecs, dtype=float)
    sims = d @ q / (np.linalg.norm(d, axis=1) * np.linalg.norm(q) + 1e-12)
    return list(np.argsort(-sims)[:k])


def _tokens(s: str) -> list[str]:
    return re.findall(r"\w+", s.lower())


def bm25_scores(query: str, docs: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
    """Оцінки BM25 запиту для кожного документа."""
    toks = [_tokens(d) for d in docs]
    avg = sum(map(len, toks)) / max(1, len(toks))
    df = Counter(t for ts in toks for t in set(ts))
    n = len(docs)
    scores = []
    for ts in toks:
        tf = Counter(ts)
        s = 0.0
        for t in set(_tokens(query)):
            if t in tf:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(ts) / avg))
        scores.append(s)
    return scores


def rrf(rankings: list[list[int]], k: int = 60) -> list[int]:
    """Злиття рангів: score(d) = сума 1 / (k + rank)."""
    score = Counter()
    for ranking in rankings:
        for r, doc in enumerate(ranking, 1):
            score[doc] += 1 / (k + r)
    return [d for d, _ in score.most_common()]


def embed(client, texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT", dim: int = 768) -> list[list[float]]:
    """Вбудовування Gemini Embedding 2 зі зменшеною розмірністю (MRL)."""
    from google.genai import types
    resp = client.models.embed_content(model=MODEL_EMBED, contents=texts,
                                       config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=dim))
    return [e.values for e in resp.embeddings]


def build_prompt(question: str, fragments: list[str]) -> str:
    """Підказка з пронумерованими фрагментами для відповіді з цитуванням."""
    ctx = "\n".join(f'<fragment id="{i}">{f}</fragment>' for i, f in enumerate(fragments, 1))
    return (f"<documents>\n{ctx}\n</documents>\n\nВідповідай лише за документами й посилайся на номери "
            f"фрагментів у квадратних дужках. Якщо відповіді немає – скажи про це.\n\nЗапитання: {question}")
