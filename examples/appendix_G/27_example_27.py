# Додаток Г. Довідник рецептів коду – приклад 27 (рукопис: 93-dodatok-g.md, рядок 509)
import time

store = client.file_search_stores.create(
    config=types.CreateFileSearchStoreConfig(display_name="Регламенти «Смереки»"))
op = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=store.name, file="reglament_adr_2026.pdf")
while not op.done:
    time.sleep(5)
    op = client.operations.get(op)

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Чи можна приймати на склад акумулятори класу 9 ADR?",
    config=types.GenerateContentConfig(tools=[types.Tool(file_search=types.FileSearch(
        file_search_store_names=[store.name], top_k=5))]),
)
for ch in resp.candidates[0].grounding_metadata.grounding_chunks or []:
    if ch.retrieved_context:
        print(ch.retrieved_context.title, "стор.", ch.retrieved_context.page_number)
