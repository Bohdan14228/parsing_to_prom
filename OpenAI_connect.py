import os
from dotenv import load_dotenv
import requests
import openai
import base64
from io import BytesIO
from PIL import Image
import json

load_dotenv()

prompt = (
        "Ты уже опытный предприниматель на украинском маркетплейсе Prom. По фото и названию продукта:"
        "\n1. Переведи название товара на украинский язык."
        "\n2. Создай описание на украинском языке, указав: тип продукта, материалы и габариты, практичность, "
        "уход (устойчивость к царапинам, чистка)."
        "\nОписание должно быть от 4 предложений, но не пиши много лишнего. Добавь теплые эмоции — кому товар подойдет."
        "\nВ описании не должно быть написано 'Название товара:' и писать его название и 'Описание товара:' и писать "
        "дальше его описание, просто одно сплошное описание которое потом можно будет вставить в маркетплейсе в "
        "строку Описание."
        "\nНе зацикливайся на названии товара, не делай описание только по нему. К примеру если название это 'Ножи "
        "деревянные', а на фото ты видишь не только их, а к примеру еще автоматы или топоры, то нужно в описании "
        "упомянуть и их."
        "\n\nВерни результат в формате JSON:\n"
        "{\n \"title_ru\": \"...\",\n  \"title_ua\": \"...\",\n  \"description_ru\": \"...\",\n  \"description_ua\": "
        "\"...\"\n}"
    )


client = openai.OpenAI(api_key=os.getenv("IA_TOKEN"))


def get_description_from_product(title: str, categories: str, image_urls: list):
    image_contents = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        image.convert("RGB").save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        image_contents.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}})

    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Ты помощник по написанию продающих описаний товаров."},
            {"role": "user", "content": [
                {"type": "text", "text": f"{prompt}\nНазвание товара: {title}, а состоит он в категории {categories}"},
                *image_contents
            ]}
        ],
        max_tokens=500
    )

    result = chat_completion.choices[0].message.content.strip()

    if result.startswith('```json'):
        result = result[7:-3].strip()

    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        print("Исходный ответ:", result)
        return "-"


