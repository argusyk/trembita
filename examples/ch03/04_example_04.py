# Розділ 3. Токени, мультимодальні токени й довгий контекст – приклад 4 (рукопис: 03-tokeny-kontekst.md, рядок 246)
from google import genai
from google.genai import types

client = genai.Client()

# Files API зберігає файли 48 год: у повторних запусках беріть їх через
# client.files.get(name=...), а не завантажуйте щоразу наново
paths = ["reglament_perevezen.pdf"] + [f"dogovory/d{i:02d}.pdf" for i in range(1, 41)]
files = [client.files.upload(file=p) for p in paths]

parts = []
for path, f in zip(paths, files):
    parts += [types.Part(text=f"<документ: {path}>"), f]   # мітка перед документом

question = (
    "Претензія SM-2610-0388: вантаж прибув до Ужгорода на три доби пізніше. "
    "Які пункти регламенту й договору з перевізником застосовні? "
    "Спершу дослівно процитуй ці пункти з назвою документа, потім дай висновок."
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[*parts, question],        # запитання – наприкінці, після документів
    config=types.GenerateContentConfig(
        system_instruction="Ти – юридичний помічник відділу претензій «Смереки».",
        max_output_tokens=16384,        # з запасом на мислення й відповідь
    ),
)
print(resp.text)
u = resp.usage_metadata
print(u.prompt_token_count, u.thoughts_token_count, u.candidates_token_count)
