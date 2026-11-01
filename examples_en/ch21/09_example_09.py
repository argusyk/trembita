# Chapter 21. Retrieval-Augmented Generation: Embeddings, File Search and RAG Engine – example 9 (manuscript: 21-rag.md, line 411)
from trembita.config import MODEL_MAIN

resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="What documents are needed to export pallets to Poland?",
    config=types.GenerateContentConfig(tools=[types.Tool(file_search=types.FileSearch(
        file_search_store_names=[store.name],
        metadata_filter="dept=customs",           # customs regulations only
        top_k=6,
    ))]),
)
print(resp.text)

gm = resp.candidates[0].grounding_metadata if resp.candidates else None
if gm:                                            # no search, no metadata
    for i, ch in enumerate(gm.grounding_chunks or []):
        rc = ch.retrieved_context
        if rc:
            print(f"[{i}] {rc.title}, p. {rc.page_number}: {(rc.text or '')[:80]}")
    for sup in gm.grounding_supports or []:
        # which piece of the answer is supported by which chunks
        print(f"“{sup.segment.text}” <- {sup.grounding_chunk_indices}")
