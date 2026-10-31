# Додаток А. Практикум – приклад 12 (рукопис: 90-dodatok-a.md, рядок 591)
import numpy as np
from trembita.client import make_client
from trembita.rag import bm25_scores, chunk, cosine_top_k, embed, rrf

client = make_client()
chunks = chunk(open("corpus.md", encoding="utf-8").read(), size=800, overlap=150)
doc_vecs = embed(client, chunks, task_type="RETRIEVAL_DOCUMENT")

def search(query: str, k: int = 5) -> dict[str, list[int]]:
    q = embed(client, [query], task_type="RETRIEVAL_QUERY")[0]
    vec = cosine_top_k(q, doc_vecs, k=20)
    lex = [int(i) for i in np.argsort(bm25_scores(query, chunks))[::-1][:20]]
    return {"vector": vec[:k], "bm25": lex[:k], "hybrid": rrf([vec, lex])[:k]}
