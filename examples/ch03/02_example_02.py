# Розділ 3. Токени, мультимодальні токени й довгий контекст – приклад 2 (рукопис: 03-tokeny-kontekst.md, рядок 152)
from google import genai

client = genai.Client()  # ключ – у змінній середовища GEMINI_API_KEY

pairs = {
    "en": "The carrier is liable for total or partial loss of the goods "
          "and for damage thereto occurring between the time when he takes "
          "over the goods and the time of delivery.",
    "uk": "Перевізник несе відповідальність за повну чи часткову втрату "
          "вантажу або за його пошкодження, що сталися з моменту прийняття "
          "вантажу до перевезення і до моменту його доставки.",
}
counts = {}
for lang, text in pairs.items():
    resp = client.models.count_tokens(model="gemini-3.8-flash", contents=text)
    counts[lang] = resp.total_tokens

k = counts["uk"] / counts["en"]
print(counts, f"коефіцієнт мови k = {k:.2f}")
