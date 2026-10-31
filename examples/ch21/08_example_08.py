# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 8 (рукопис: 21-rag.md, рядок 422)
def evaluate_retrieval(golden: list[dict], search, k: int = 6) -> dict:
    """golden: [{"q": питання, "rel": множина id релевантних фрагментів}]."""
    recalls, rr = [], []
    for item in golden:
        found = [chunks[i]["id"] for i in search(item["q"])[:k]]
        hits = [j for j, cid in enumerate(found, start=1) if cid in item["rel"]]
        recalls.append(len(set(found) & item["rel"]) / len(item["rel"]))
        rr.append(1 / hits[0] if hits else 0.0)
    return {"recall@k": float(np.mean(recalls)), "mrr": float(np.mean(rr))}


print(evaluate_retrieval(golden, lambda q: hybrid_search(q, vindex, bm25)))
