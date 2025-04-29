from fastapi import Request
from transformers import pipeline

translator_map = {
    "fr": pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr"),  # English to French
    "de": pipeline("translation", model="Helsinki-NLP/opus-mt-en-de"),  # English to German
    "es": pipeline("translation", model="Helsinki-NLP/opus-mt-en-es"),  # English to Spanish
    "hi": pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi"),  # English to Hindi
}

async def translate(request: Request):
    form_data = await request.form()
    text = form_data.get("text")
    target_language = form_data.get("target_language")

    if not text or not target_language:
        return {"error": "Text and target language must be provided"}

    translator = translator_map.get(target_language)
    if translator is None:
        return {"error": "Target language not supported"}

    try:
        translated_text = translator(text, max_length=40)
        return {"translated_text": translated_text[0]['translation_text']}
    except Exception as e:
        return {"error": str(e)}