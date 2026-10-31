# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 6 (рукопис: 21-rag.md, рядок 324)
import time
from pathlib import Path

store = client.file_search_stores.create(
    config=types.CreateFileSearchStoreConfig(display_name="smereka-reglamenty"))


def upload(path: str, dept: str, year: int) -> None:
    op = client.file_search_stores.upload_to_file_search_store(
        file_search_store_name=store.name,
        file=path,
        config=types.UploadToFileSearchStoreConfig(
            display_name=Path(path).name,
            custom_metadata=[
                types.CustomMetadata(key="dept", string_value=dept),
                types.CustomMetadata(key="year", numeric_value=year),
            ],
            chunking_config=types.ChunkingConfig(
                white_space_config=types.WhiteSpaceConfig(
                    max_tokens_per_chunk=400, max_overlap_tokens=40)),
        ),
    )
    while not op.done:                  # індексація – довга операція
        time.sleep(3)
        op = client.operations.get(op)
    if op.error:
        raise RuntimeError(f"{path}: {op.error}")


upload("reglamenty/mytne-oformlennia.pdf", dept="customs", year=2026)
upload("reglamenty/pretenzii.docx", dept="claims", year=2025)
