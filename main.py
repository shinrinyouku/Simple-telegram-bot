import telebot
from telebot import types
import sqlite3
import random
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

jokes = [
    "Почему программисты так не любят перерывы? Потому что они боятся, что их код выйдет из компиляции.",
    "Как программист снимает стресс? Пишет на бумаге 'print(\"Hello World\")'.",
    "Почему серверы никогда не отдыхают? Потому что они всегда в режиме ожидания.",
    "Я пытался отладить жизнь, но не смог найти точку входа."
]

def get_suggestion(category, genre):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    if category == "audiobooks":
        c.execute("SELECT title, image_url, audio_url FROM audiobooks WHERE genre=?", (genre,))
    else:
        c.execute(f"SELECT title, image_url FROM {category} WHERE genre=?", (genre,))
    results = c.fetchall()
    conn.close()
    return random.choice(results) if results else None

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("\U0001F4DA Книга", "\U0001F4D6 Манга", "\U0001F4D5 Комикс", "\U0001F3A7 Аудиокнига", "🎉 Пасхалка")
    bot.send_message(message.chat.id, "Привет! Что хочешь почитать/послушать?", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["\U0001F4DA Книга", "\U0001F4D6 Манга", "\U0001F4D5 Комикс", "\U0001F3A7 Аудиокнига"])
def handle_category(message):
    category_map = {
        "\U0001F4DA Книга": "books",
        "\U0001F4D6 Манга": "manga",
        "\U0001F4D5 Комикс": "comics",
        "\U0001F3A7 Аудиокнига": "audiobooks"
    }
    category = category_map[message.text]
    genre_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    genre_markup.add("фэнтези", "детектив", "романтика", "\U0001F519 Назад", "🎉 Пасхалка")
    bot.send_message(message.chat.id, f"Выбери жанр для {message.text.lower()}:", reply_markup=genre_markup)
    bot.register_next_step_handler(message, lambda m: genre_handler(m, category))

@bot.message_handler(func=lambda m: m.text == "🎉 Пасхалка")
def send_easter_egg_video(message):
    try:
        with open("C:/Users/админ/Desktop/daddy/game/Bot/888,.mp4", "rb") as video:
            bot.send_video(message.chat.id, video)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "❌ Видео пасхалки не найдено.")

@bot.message_handler(func=lambda m: m.text == "\U0001F519 Назад")
def back_to_start(message):
    start_handler(message)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Привет! Я — бот для поиска книг, манги, комиксов и аудиокниг.\n"
        "Вот что я умею:\n"
        "/start — начать использование бота\n"
        "Выберите категорию:\n"
        "📚 Книга\n"
        "📖 Манга\n"
        "📙 Комикс\n"
        "🎧 Аудиокнига\n"
        "После этого я помогу выбрать жанр и найду для вас произведение.\n"
        "Также есть секретная кнопка, которая отправит вам удивительное видео! 😉"
    )
    bot.send_message(message.chat.id, help_text)

def genre_handler(message, category):
    if message.text == "\U0001F519 Назад":
        start_handler(message)
        return

    suggestion = get_suggestion(category, message.text.lower())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("\U0001F519 Назад")

    if not suggestion:
        bot.send_message(message.chat.id, "Ничего не найдено по этому жанру.", reply_markup=markup)
        return

    if category == "audiobooks":
        title, image_url, audio_url = suggestion
        if image_url:
            bot.send_photo(message.chat.id, image_url, caption=title)
        if audio_url:
            try:
                bot.send_audio(message.chat.id, audio_url, caption="\U0001F3A7 Слушай прямо здесь", reply_markup=markup)
            except:
                bot.send_message(message.chat.id, f"{title}\n(⚠️ Не удалось загрузить аудио)", reply_markup=markup)
    else:
        title, image_url = suggestion
        if image_url:
            try:
                bot.send_photo(message.chat.id, image_url, caption=f"Советую: {title}", reply_markup=markup)
            except:
                bot.send_message(message.chat.id, f"Советую: {title}\n(⚠️ Не удалось загрузить изображение)", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"Советую: {title}", reply_markup=markup)

    joke_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    joke_markup.add("Да", "Нет")
    bot.send_message(message.chat.id, "Хотите анекдот?", reply_markup=joke_markup)
    bot.register_next_step_handler(message, handle_joke_response)

def handle_joke_response(message):
    if message.text == "Да":
        joke = random.choice(jokes)
        bot.send_message(message.chat.id, joke)
        genre_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        genre_markup.add("фэнтези", "детектив", "романтика", "\U0001F519 Назад", "🎉 Пасхалка")
        bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=genre_markup)
        bot.register_next_step_handler(message, lambda m: genre_handler(m, "books"))
    elif message.text == "Нет":
        start_handler(message)

bot.polling(none_stop=True)
