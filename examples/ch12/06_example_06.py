# Розділ 12. Заземлення та вбудовані інструменти – приклад 6 (рукопис: 12-zazemlennia.md, рядок 246)
import time
from google import genai
from google.genai import types

client = genai.Client()

store = client.file_search_stores.create(
    config=types.CreateFileSearchStoreConfig(display_name="Регламенти «Смереки»"))

op = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=store.name,
    file="reglament_nebezpechni_vantazhi_2026.pdf",
    config=types.UploadToFileSearchStoreConfig(
        display_name="Небезпечні вантажі (ADR), ред. 2026",
        custom_metadata=[types.CustomMetadata(key="viddil", string_value="sklad")],
    ),
)
while not op.done:                     # індексування займає секунди або хвилини
    time.sleep(5)
    op = client.operations.get(op)

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Чи можна приймати на львівський склад акумулятори клас 9 ADR без попередження?",
    config=types.GenerateContentConfig(tools=[types.Tool(
        file_search=types.FileSearch(file_search_store_names=[store.name], top_k=5))]),
)
print(resp.text)
meta = resp.candidates[0].grounding_metadata
for ch in (meta.grounding_chunks or []) if meta else []:
    rc = ch.retrieved_context
    if rc:
        print(rc.title, "стор.", rc.page_number)
