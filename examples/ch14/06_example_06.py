# Розділ 14. Live API і генерація медіа – приклад 6 (рукопис: 14-live-media.md, рядок 273)
from google import genai
from google.genai import types

client = genai.Client()
IMG = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"],
                                  image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"))


def save_images(resp, prefix: str) -> None:
    for i, part in enumerate(resp.parts):
        if part.text:
            print(part.text)                      # модель може коментувати результат
        elif part.inline_data:
            part.as_image().save(f"{prefix}_{i}.png")


# 1) Нове зображення з тексту
save_images(client.models.generate_content(
    model="gemini-3.1-flash-image", config=IMG,
    contents="Схематична ілюстрація для інструкції водіям: як закріпити палети в напівпричепі "
             "ременями з храповиком. Чисті лінії, світлий фон, без написів."), "kriplennia")

# 2) Редагування наявного плаката в розмові
chat = client.chats.create(model="gemini-3.1-flash-image", config=IMG)
with open("plakat_sklad_uzhhorod.png", "rb") as f:
    poster = types.Part.from_bytes(data=f.read(), mime_type="image/png")
chat.send_message([poster, "Переклади всі написи англійською, стиль і розміщення збережи."])
save_images(chat.send_message("Тепер зроби фон світлішим, а логотип «Смереки» трохи меншим."), "plakat_en")
