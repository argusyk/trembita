# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 9 (рукопис: 21-rag.md, рядок 411)
from trembita.config import MODEL_MAIN

resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Які документи потрібні для експорту палет до Польщі?",
    config=types.GenerateContentConfig(tools=[types.Tool(file_search=types.FileSearch(
        file_search_store_names=[store.name],
        metadata_filter="dept=customs",           # лише митні регламенти
        top_k=6,
    ))]),
)
print(resp.text)

gm = resp.candidates[0].grounding_metadata if resp.candidates else None
if gm:                                            # без пошуку метаданих немає
    for i, ch in enumerate(gm.grounding_chunks or []):
        rc = ch.retrieved_context
        if rc:
            print(f"[{i}] {rc.title}, с. {rc.page_number}: {(rc.text or '')[:80]}")
    for sup in gm.grounding_supports or []:
        # який шматок відповіді якими фрагментами підкріплено
        print(f"«{sup.segment.text}» <- {sup.grounding_chunk_indices}")
