# Appendix D. Code Recipes – example 27 (manuscript: 93-appendix-d.md, line 518)
import time

store = client.file_search_stores.create(
    config=types.CreateFileSearchStoreConfig(display_name="Smereka regulations"))
op = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=store.name, file="reglament_adr_2026.pdf")
while not op.done:
    time.sleep(5)
    op = client.operations.get(op)

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="May ADR class 9 batteries be accepted into the warehouse?",
    config=types.GenerateContentConfig(tools=[types.Tool(file_search=types.FileSearch(
        file_search_store_names=[store.name], top_k=5))]),
)
meta = resp.candidates[0].grounding_metadata if resp.candidates else None
for ch in (meta.grounding_chunks or []) if meta else []:
    if ch.retrieved_context:
        print(ch.retrieved_context.title, "p.", ch.retrieved_context.page_number)
