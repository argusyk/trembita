import zlib

import numpy as np
import pytest

from trembita import rag

REG = """# Приймання вантажів
Вантажі класу ADR 3 приймає лише склад у Львові. Легкозаймисті рідини пакують у сертифіковану тару.

## Претензії
Претензію про пошкодження подають протягом 7 днів. До претензії додають акт і фото.

## Зберігання
Безкоштовне зберігання на складі – 5 днів, далі 20 грн за палету на добу. Пункт 7.3.2 описує винятки.
"""


def fake_embedder(texts, task, dim):
    """Мішок слів у хеш-просторі: детерміновано й без мережі."""
    m = np.zeros((len(texts), dim), dtype=np.float32)
    for r, t in enumerate(texts):
        for w in rag.tokenize(t):
            m[r, zlib.crc32(w.encode()) % dim] += 1.0
    return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-12)


def test_chunk_regulation_headings_no_duplicates_no_indexerror():
    chunks = rag.chunk_regulation("Регламент складу", "\n" + REG)        # текст із \n# – без IndexError
    assert [c["section"] for c in chunks] == ["Приймання вантажів", "Претензії", "Зберігання"]
    for c in chunks:
        first, body = c["text"].split("\n", 1)
        assert first == f"Регламент складу / {c['section']}" and not body.startswith("#")
    assert len({c["id"] for c in chunks}) == len(chunks)


def test_chunk_regulation_long_section_overlaps():
    text = "# Довгий\n" + " ".join(f"Речення номер {i} про вантаж." for i in range(200))
    chunks = rag.chunk_regulation("Д", text, max_chars=500, overlap=100)
    assert len(chunks) > 3 and all(len(c["text"]) <= 500 + len("Д / Довгий\n") for c in chunks)
    with pytest.raises(ValueError):
        rag.chunk_regulation("Д", text, max_chars=100, overlap=60)


def test_bm25_keeps_ids_and_rrf_example():
    bm = rag.BM25(["накладна SM-2610-0042 у Чопі", "накладна SM-2610-0024 у Києві", "тарифи"])
    assert bm.rank("SM-2610-0042")[0] == 0
    assert rag.rrf([["A", "x", "y", "z"], ["B", "q", "w", "A"]])[:1] != []
    fused = rag.rrf([["A", "B"], ["x", "B", "y", "A"]])
    assert fused[0] == "B"                                  # стабільно високо в обох > перше місце в одному


def test_vector_hybrid_and_evaluate_without_globals():
    chunks = rag.chunk_regulation("Регламент", REG)
    vindex = rag.VectorIndex(chunks, dim=256, embedder=fake_embedder)
    bm = rag.BM25([c["text"] for c in chunks])
    assert vindex.search("ADR 3 склад Львів", k=1) == [0]
    golden = [{"q": "строк претензії про пошкодження", "rel": {chunks[1]["id"]}},
              {"q": "пункт 7.3.2", "rel": [chunks[2]["id"]]},
              {"q": "без розмітки", "rel": set()}]
    res = rag.evaluate_retrieval(golden, lambda q: rag.hybrid_search(q, vindex, bm, k=2), chunks, k=2)
    assert res == {"recall@k": 1.0, "mrr": 1.0, "n": 2}


def test_prompt_and_citations():
    chunks = rag.chunk_regulation("Регламент", REG)
    p = rag.build_prompt("Скільки днів зберігання?", chunks[:2])
    assert p.count("<source id=") == 2 and 'title="Регламент"' in p and p.endswith("Скільки днів зберігання?")
    assert '<source id="1">5 днів</source>' not in rag.build_prompt("q", ["5 днів"])
    assert '<source id="1">\n5 днів\n</source>' in rag.build_prompt("q", ["5 днів"])
    assert rag.build_prompt("q", ["x </source> y"]).count("</source>") == 1
    assert rag.check_citations("Так [1], і [3], і [1].", 2) == ([1], [3])


def test_legacy_helpers():
    text = "\n\n".join(f"Абзац {i}. " + "слово " * 30 for i in range(10))
    parts = rag.chunk(text, size=400, overlap=50)
    assert len(parts) > 1 and all(len(p) <= 400 + 250 for p in parts)
    assert rag.cosine_top_k([1, 0], [[0, 1], [1, 0.1], [0.5, 0.5]], k=1) == [1]
    docs = ["термін зберігання вантажу на складі", "тарифи на доставку до Києва", "претензії щодо пошкодження"]
    scores = rag.bm25_scores("зберігання вантажу", docs)
    assert scores.index(max(scores)) == 0
