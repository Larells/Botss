import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from questions_answers import USER_PROMPTS, BOT_RESPONSES

# Память пользователей
user_data = {}

# Кнопки
gender_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("🧑 Я парень"), KeyboardButton("👩 Я девушка")]
], resize_keyboard=True)

main_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("📜 Расскажи мне историю"), KeyboardButton("😂 Анекдот")],
    [KeyboardButton("🧭 Меню"), KeyboardButton("💌 Подписка")],
    [KeyboardButton("🎲 Случайный факт")]
], resize_keyboard=True)

short_stories = [
    "Он однажды ушёл в никуда, чтобы найти себя. И нашёл.",
    "Была зима, всё вокруг было пусто, но внутри — надежда.",
    "Никто не верил, но она смогла. Потому что не сдавалась.",
]

jokes = [
    "— Почему бот не пошёл на свидание?\n— У него зависло сердце 💔",
    "— Я прокачал интеллект!\n— А харизму?\n— Ну, у меня же бот.",
]

facts = [
    "Женский мозг активнее в состоянии покоя, чем мужской.",
    "Сердце человека действительно может «болеть» от стресса.",
    "Роботы пока не умеют любить... но я учусь 😉",
]

# Ответы по полу
male_responses = [
    "Понял тебя, бро. Давай подробнее.",
    "Звучит интересно, расскажи ещё!",
    "Норм тема! А что дальше?",
    "Ты прям мужик с мыслями 💪",
]

female_responses = [
    "Звучит очень искренне ❤️",
    "Ты умеешь делиться настоящим 🌸",
    "Мне приятно тебя слушать 😌",
    "Ты очень милая, правда 💖",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"gender": None}
    await update.message.reply_text(
        "Привет! Я твой бот-друг 🧠 Перед тем как продолжим, скажи, кто ты:",
        reply_markup=gender_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Пол не выбран — определим
    if user_id not in user_data:
        user_data[user_id] = {"gender": None}

    if user_data[user_id]["gender"] is None:
        if "парень" in text:
            user_data[user_id]["gender"] = "male"
            await update.message.reply_text("Отлично, брат! Теперь можем общаться!", reply_markup=main_keyboard)
            return
        elif "девушка" in text:
            user_data[user_id]["gender"] = "female"
            await update.message.reply_text("Прекрасно! Очень рада общаться 🌸", reply_markup=main_keyboard)
            return
        else:
            await update.message.reply_text("Пожалуйста, выбери — ты парень или девушка?", reply_markup=gender_keyboard)
            return

    gender = user_data[user_id]["gender"]

    # Команды
    if "меню" in text:
        await update.message.reply_text("Вот что я умею:", reply_markup=main_keyboard)
    elif "истори" in text:
        await update.message.reply_text("📖 История:\n\n" + random.choice(short_stories))
    elif "анекдот" in text:
        await update.message.reply_text("😂 Анекдот:\n\n" + random.choice(jokes))
    elif "pluse+" in text:
        await update.message.reply_text("Ты уже подписан на моё сердце 💌")
    elif "факт" in text:
        await update.message.reply_text("🎲 Факт:\n\n" + random.choice(facts))
    else:
        # Обычное сообщение
        response = random.choice(male_responses if gender == "male" else female_responses)
        question = random.choice(USER_PROMPTS)
        await update.message.reply_text(f"{response}\n\n{question}")

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("Ошибка: BOT_TOKEN не установлен.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()