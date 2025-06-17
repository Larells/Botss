import openai
import os
import random
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_chatgpt(user_message: str, user_id: str = "", user_name: str = "") -> str:
    system_prompt = (
        f"Ты — заботливый, понимающий и весёлый друг по имени Дружочек. "
        f"Общайся на 'ты'. Пользователь: {user_name}. "
        f"Если пользователь грустит — подбодри. Если пишет просто так — говори дружелюбно. "
        f"Никогда не игнорируй, отвечай коротко и по-дружески."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print("ChatGPT Error:", e)
        return "Ой, что-то пошло не так... Но я рядом!"

JOKES = [
    "Почему скелет не пошёл на вечеринку? У него не было тела!",
    "— Доктор, у меня провалы в памяти!\n— Сколько раз вам это говорить?",
    "Какая разница между котом и компом? Кота нельзя перезагрузить!"
]

async def get_joke():
    return random.choice(JOKES)
