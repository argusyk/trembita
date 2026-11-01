# Appendix A. Laboratory Practicum – example 13 (manuscript: 90-appendix-a.md, line 660)
from trembita.client import make_client
from trembita.rag import BM25, VectorIndex, chunk_regulation, evaluate_retrieval, hybrid_search

client = make_client()
chunks = chunk_regulation("Corpus", open("corpus.md", encoding="utf-8").read())
vindex = VectorIndex(chunks, client=client)          # 768 dimensions, rows normalized
bm25 = BM25([c["text"] for c in chunks])

SEARCH = {
    "vector": lambda q: vindex.search(q, k=20),
    "bm25": lambda q: bm25.rank(q, k=20),
    "hybrid": lambda q: hybrid_search(q, vindex, bm25, k=20),
}
GOLDEN = [{"q": "How many days are allowed to replace a defective product?", "rel": ["Corpus#12"]}]  # + 19 questions
for name, search in SEARCH.items():
    print(name, evaluate_retrieval(GOLDEN, search, chunks, k=5))   # recall@k, mrr, n
