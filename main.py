import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from questions_answers import USER_PROMPTS, BOT_RESPONSES

# Временная память
user_data = {}

# Игровые состояния
guess_number_game = {}

# Кнопки
main_keyboard = ReplyKeyboardMarkup([
    ["📜 История", "😂 Анекдот"],
    ["🎮 Игры", "🧠 Кто я?"],
    ["🧩 Случайный факт", "💌 Подписка"]
], resize_keyboard=True)

games_keyboard = ReplyKeyboardMarkup([
    ["🎲 Угадай число", "🎱 Шар судьбы"],
    ["🃏 Правда или действие", "🔙 Назад"]
], resize_keyboard=True)

stories = [
    "Когда он остался один в городе, он понял, что одиночество — это не проклятие, а шанс познакомиться с собой.",
    "Она шла под дождём без зонта. Просто потому что слёзы никто не увидит под каплями.",
    "Иногда нужно потеряться, чтобы найти путь, который всегда был твоим.",
]

jokes = [
    "— Почему бот не ходит в спортзал?\n— У него нет тела, только душа 😅",
    "— Я проснулся и сразу лёг.\n— Это как?\n— Встал с дивана, лёг в депрессию.",
    "— У меня аллергия на понедельники. Симптомы: работа и отчаяние.",
    "— Знаешь, зачем мне зарядка по утрам?\n— Чтобы не уснуть навсегда.",
]

facts = [
    "У мозга нет болевых рецепторов — сам мозг не чувствует боли.",
    "Сердце действительно может «разорваться» от сильной эмоции.",
    "Мозг работает активнее во сне, чем когда ты смотришь TikTok.",
]

truth_or_dare = [
    "Правда: Ты когда-нибудь притворялся, что спишь, чтобы избежать разговора?",
    "Правда: Есть ли у тебя секрет, о котором никто не знает?",
    "Действие: Скажи комплимент сам себе.",
    "Правда: Была ли у тебя влюблённость в вымышленного персонажа?",
    "Действие: Напиши сообщение человеку, которому ты давно не писал.",
]

magic_ball = [
    "Без сомнений.",
    "Скоро произойдёт.",
    "Не надейся.",
    "Лучше не знать ответа.",
    "Скоро всё изменится.",
    "Ты уже знаешь ответ в глубине души.",
]

def get_gender_emoji(gender):
    return "🧑" if gender == "male" else "👩"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.effective_user.first_name
    if user_id not in user_data:
        user_data[user_id] = {
            "name": name,
            "gender": None,
            "last_topics": []
        }
    await update.message.reply_text(
        f"Привет, {name}! 🙌 Я твой бот-друг. Напиши, кто ты:",
        reply_markup=ReplyKeyboardMarkup(
            [["🧑 Я парень", "👩 Я девушка"]],
            resize_keyboard=True
        )
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    user = user_data.setdefault(user_id, {"name": "Друг", "gender": None, "last_topics": []})

    # Определение пола
    if user["gender"] is None:
        if "парень" in message.lower():
            user["gender"] = "male"
            await update.message.reply_text("Отлично, брат! Давай болтать 🔥", reply_markup=main_keyboard)
            return
        elif "девушка" in message.lower():
            user["gender"] = "female"
            await update.message.reply_text("Круто! Я рад нашему знакомству 💖", reply_markup=main_keyboard)
            return
        else:
            await update.message.reply_text("Выбери пол, чтобы продолжить 🙃")
            return

    gender = user["gender"]
    name = user["name"]

    # Игры
    if message == "🎮 Игры":
        await update.message.reply_text("Выбери игру 🎲", reply_markup=games_keyboard)
    elif message == "🔙 Назад":
        await update.message.reply_text("Возвращаемся к основному меню:", reply_markup=main_keyboard)
    elif message == "🎲 Угадай число":
        number = random.randint(1, 5)
        guess_number_game[user_id] = number
        await update.message.reply_text("Я загадал число от 1 до 5. Попробуй угадать!")
    elif message.isdigit() and user_id in guess_number_game:
        correct = guess_number_game[user_id]
        guess = int(message)
        if guess == correct:
            await update.message.reply_text("Угадал! 🎉 Красавчик!")
        else:
            await update.message.reply_text(f"Неа! Я загадал {correct} 😜")
        del guess_number_game[user_id]
    elif message == "🃏 Правда или действие":
        await update.message.reply_text(random.choice(truth_or_dare))
    elif message == "🎱 Шар судьбы":
        await update.message.reply_text(random.choice(magic_ball))

    # Основное меню
    elif "анекдот" in message.lower():
        await update.message.reply_text("😂 Анекдот:\n\n" + random.choice(jokes))
    elif "истори" in message.lower():
        await update.message.reply_text("📜 История:\n\n" + random.choice(stories))
    elif "подпис" in message.lower():
        await update.message.reply_text("Ты уже со мной. А это лучшая подписка 💌")
    elif "факт" in message.lower():
        await update.message.reply_text("🧩 Факт:\n\n" + random.choice(facts))
    elif "меню" in message.lower():
        await update.message.reply_text("Вот что я умею:", reply_markup=main_keyboard)
    elif "кто я" in message.lower():
        g = "парень" if gender == "male" else "девушка"
        topics = ", ".join(user["last_topics"][-3:]) or "ничего особо"
        await update.message.reply_text(f"Ты — {g}, тебя зовут {name}, мы говорили о: {topics}")
    else:
        # Обычное сообщение
        user["last_topics"].append(message)
        response = random.choice(BOT_RESPONSES)
        question = random.choice(USER_PROMPTS)
        await update.message.reply_text(f"{response}\n\n{question}")

def main():
    import os
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Ошибка: BOT_TOKEN не установлен")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()