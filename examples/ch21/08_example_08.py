# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 8 (рукопис: 21-rag.md, рядок 382)
from pathlib import Path
from google.genai import types
from trembita.client import make_client

client = make_client(timeout_ms=120_000)     # великий PDF вантажиться довше за типові 20 с


def upload_config(path: str, dept: str, year: int) -> types.UploadToFileSearchStoreConfig:
    """Метадані для фільтра і власне розбиття: 400 токенів, перекриття 40 (10 %)."""
    return types.UploadToFileSearchStoreConfig(
        display_name=Path(path).name,
        custom_metadata=[types.CustomMetadata(key="dept", string_value=dept),
                         types.CustomMetadata(key="year", numeric_value=year)],
        chunking_config=types.ChunkingConfig(white_space_config=types.WhiteSpaceConfig(
            max_tokens_per_chunk=400, max_overlap_tokens=40)),
    )


store = client.file_search_stores.create(
    config=types.CreateFileSearchStoreConfig(display_name="smereka-reglamenty"))
path = "reglamenty/mytne-oformlennia.pdf"
op = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=store.name, file=path, config=upload_config(path, "customs", 2026))
# далі – очікування op.done через client.operations.get, як у підрозділі 12.6
