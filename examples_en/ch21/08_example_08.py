# Chapter 21. Retrieval-Augmented Generation: Embeddings, File Search and RAG Engine – example 8 (manuscript: 21-rag.md, line 382)
from pathlib import Path
from google.genai import types
from trembita.client import make_client

client = make_client(timeout_ms=120_000)     # a large PDF takes longer to upload than the default 20 s


def upload_config(path: str, dept: str, year: int) -> types.UploadToFileSearchStoreConfig:
    """Metadata for the filter and custom chunking: 400 tokens, overlap 40 (10%)."""
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
# then wait for op.done via client.operations.get, as in Section 12.6
