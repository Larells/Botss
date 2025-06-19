import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from questions_answers import USER_PROMPTS, BOT_RESPONSES

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой бот-друг 😊 Давай поговорим. Напиши что-нибудь!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    greetings = ['привет', 'здравствуй', 'хай', 'hello', 'hi']
    sad_words = ['плохо', 'грустно', 'уныло', 'печаль']
    good_words = ['нормально', 'хорошо', 'ок', 'супер', 'отлично']

    if any(word in user_text for word in greetings):
        await update.message.reply_text("Привет! Как у тебя дела?")
    elif any(word in user_text for word in sad_words):
        await update.message.reply_text("Мне жаль это слышать 😔 Если хочешь, можешь рассказать подробнее.")
    elif any(word in user_text for word in good_words):
        await update.message.reply_text("Рад это слышать! Что нового у тебя?")
    else:
        response = random.choice(BOT_RESPONSES)
        question = random.choice(USER_PROMPTS)
        await update.message.reply_text(f"{response}\n\n{question}")

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("Ошибка: BOT_TOKEN не установлен в переменных окружения")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
