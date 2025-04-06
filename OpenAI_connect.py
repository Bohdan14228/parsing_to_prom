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
    "Ты эксперт по созданию продающих описаний для маркетплейсов. По фото и названию товара создай краткое описание ("
    "3-4 предложения).\n"
    "**Обязательно укажи:**\n"
    "- Тип товара и материалы\n"
    "- Габариты (если видны на фото)\n"
    "- Практичность и особенности использования\n"
    "- Уход (если требуется)\n"
    "- Кому подойдет (добавь теплые эмоции)\n"
    "Не зацикливайся на названии товара, не делай описание только по нему. К примеру если название это 'Ножи "
    "деревянные', а на фото ты видишь не только их, а к примеру еще автоматы или топоры, то нужно в описании "
    "упомянуть и их. И не нужно самому дописывать исходные данный которые дают, то есть если есть название , "
    "то не нужно в нем дописывать еще что-то свое. Не нужно упоминать детали которые видишь на фото,"
    "к примеру: Ночник с зайце, про зайца писать в описании не нужно. Магниты с городом Львов, про сам город тоже "
    "ничего говорит не нужно, говори про общие характеристики товара.\n"
    "**Формат ответа:** Только JSON строго в таком формате:\n"
    "{\n"
    "  \"title_ru\": \"название на русском\",\n"
    "  \"title_ua\": \"название на украинском\",\n"
    "  \"description_ru\": \"описание на русском\",\n"
    "  \"description_ua\": \"описание на украинском\",\n"
    "}\n"
    "Не добавляй никаких пояснений, только чистый JSON."
)

client = openai.OpenAI(api_key=os.getenv("IA_TOKEN"))


def get_description_from_product(title: str, image_urls: list, description: str):
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
                {"type": "text", "text": f"{prompt}\nНазвание товара: {title}, и вот я тебе еще передам переменную с"
                                         f" описанием товара, если она есть просто вставить в конец описания с новой "
                                         f"строки, если будет '-', то ничего не нужно делать. Описание: {description}"},
                *image_contents
            ]}
        ],
        max_tokens=1000
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


t = "Магнит маленький"
i = ["https://shop.tira.com.ua/wp-content/uploads/2024/09/%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5_viber_2024-08-19_18-13-22-258.jpg"]
d = "-"

r = get_description_from_product(t, i, d)
print(r)
