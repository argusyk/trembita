# Додаток Г. Довідник рецептів коду – приклад 39 (рукопис: 93-dodatok-g.md, рядок 783)
from google.genai import errors

try:
    resp = client.models.generate_content(model="gemini-3.8-flash", contents="Привіт!")
except errors.ClientError as e:                  # 4xx
    if e.code != 429:
        raise                                    # помилка в запиті, повтор не допоможе
    print("квоту вичерпано, повторити із затримкою:", e.message)
except errors.ServerError as e:                  # 5xx
    print("тимчасовий збій сервера:", e.code, e.status)
