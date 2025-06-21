import os
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загружаем ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Память (в ОЗУ)
user_contexts = {}

# Главное меню
main_keyboard = ReplyKeyboardMarkup([
    ["📜 История", "😂 Анекдот"],
    ["🎮 Игры", "🧠 Кто я?"],
    ["🧩 Факт", "💌 Подписка"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_contexts[user.id] = []
    await update.message.reply_text(
        f"Привет, {user.first_name}! 🧠 Я бот с интеллектом. Пиши мне — и поговорим!",
        reply_markup=main_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if user.id not in user_contexts:
        user_contexts[user.id] = []

    user_contexts[user.id].append({"role": "user", "content": text})
    user_contexts[user.id] = user_contexts[user.id][-10:]  # обрезаем контекст до 10 сообщений

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # можно заменить на gpt-4
            messages=[
                {"role": "system", "content": "Ты — дружелюбный Telegram-бот, поддерживаешь разговор, шутишь, помогаешь, общаешься с подростками."},
                *user_contexts[user.id]
            ],
            temperature=0.8
        )
        reply = response.choices[0].message["content"]
except Exception as e:
    print("Ошибка OpenAI:", e)
    reply = "Интеллект сейчас не работает. Причина в консоли."

    user_contexts[user.id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот с интеллектом запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()