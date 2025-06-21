from fastapi import FastAPI, Request
import os
import openai
from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Инициализация FastAPI
app = FastAPI()

# Загружаем переменные
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://your-render-app.onrender.com/webhook

# Настройка OpenAI
openai.api_key = OPENAI_KEY

# Создание бота
application = ApplicationBuilder().token(BOT_TOKEN).build()
bot = application.bot

# Память для диалога
user_contexts = {}

# Главное меню
main_keyboard = ReplyKeyboardMarkup([
    ["📜 История", "😂 Анекдот"],
    ["🎮 Игры", "🧠 Кто я?"],
    ["🧩 Факт", "💌 Подписка"]
], resize_keyboard=True)

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_contexts[user.id] = []
    await update.message.reply_text(
        f"Привет, {user.first_name}! 🧠 Я бот с интеллектом. Пиши мне — и поговорим!",
        reply_markup=main_keyboard
    )

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if user.id not in user_contexts:
        user_contexts[user.id] = []

    user_contexts[user.id].append({"role": "user", "content": text})
    user_contexts[user.id] = user_contexts[user.id][-10:]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — дружелюбный Telegram-бот, поддерживаешь разговор, шутишь, помогаешь, общаешься с подростками."},
                *user_contexts[user.id]
            ],
            temperature=0.8
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        print("Ошибка OpenAI:", e)
        reply = "Интеллект сейчас не работает."

    user_contexts[user.id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

# Регистрация хендлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Endpoint FastAPI для Telegram webhook
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.update_queue.put(update)
    return {"ok": True}

# Установка webhook при старте
@app.on_event("startup")
async def startup():
    await bot.delete_webhook()
    await bot.set_webhook(url=WEBHOOK_URL)
    print("Webhook установлен на:", WEBHOOK_URL)