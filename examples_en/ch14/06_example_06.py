# Chapter 14. The Live API and media generation – example 6 (manuscript: 14-live-media.md, line 292)
from google import genai
from google.genai import types
from trembita.config import MODEL_IMAGE                # gemini-3.1-flash-image (Nano Banana 2)

client = genai.Client()
IMG = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"],
                                  image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"))


def save_images(resp, prefix: str) -> None:
    for i, part in enumerate(resp.parts or []):     # a blocked response has no parts
        if part.text:
            print(part.text)                      # the model may comment on the result
        elif part.inline_data:
            part.as_image().save(f"{prefix}_{i}.png")


# 1) A new image from text
save_images(client.models.generate_content(
    model=MODEL_IMAGE, config=IMG,
    contents="Schematic illustration for a drivers' manual: how to secure pallets in a semi-trailer "
             "with ratchet straps. Clean lines, light background, no text."), "kriplennia")

# 2) Editing an existing poster in a conversation
chat = client.chats.create(model=MODEL_IMAGE, config=IMG)
with open("plakat_sklad_uzhhorod.png", "rb") as f:
    poster = types.Part.from_bytes(data=f.read(), mime_type="image/png")
save_images(chat.send_message([poster, "Translate all the text into English, keep the style and layout."]),
            "plakat_en_v1")                         # each version is saved under its own prefix
save_images(chat.send_message("Now make the background lighter and the Smereka logo a little smaller."), "plakat_en_v2")
