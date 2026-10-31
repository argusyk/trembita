from trembita import rag


def test_chunk_respects_size():
    text = "\n\n".join(f"Абзац {i}. " + "слово " * 30 for i in range(10))
    parts = rag.chunk(text, size=400, overlap=50)
    assert len(parts) > 1 and all(len(p) <= 400 + 250 for p in parts)


def test_cosine_and_bm25_and_rrf():
    assert rag.cosine_top_k([1, 0], [[0, 1], [1, 0.1], [0.5, 0.5]], k=1) == [1]
    docs = ["термін зберігання вантажу на складі", "тарифи на доставку до Києва", "претензії щодо пошкодження"]
    scores = rag.bm25_scores("зберігання вантажу", docs)
    assert scores.index(max(scores)) == 0
    assert rag.rrf([[0, 1, 2], [2, 0, 1]])[0] == 0


def test_prompt_contains_fragments():
    p = rag.build_prompt("Скільки днів зберігання?", ["5 днів безкоштовно"])
    assert '<fragment id="1">5 днів безкоштовно</fragment>' in p
