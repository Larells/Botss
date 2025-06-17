import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
import os

from handlers import handle_message

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я Дружочек — твой друг и собеседник 🤗\nНажимай кнопки или просто пиши мне!",
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Мне грустно", "Поговори со мной", "Расскажи анекдот")
    )

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def all_messages(message: types.Message):
    await handle_message(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
