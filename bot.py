import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

playlists = {
    "Учёбой": {
        "Спокойствие": "https://music.yandex.ru/users/yamusic-bestsongs/playlists/13228079?utm_medium=copy_link",
        "Стресс": "https://music.yandex.ru/artist/12428168?utm_medium=copy_link",
        "Радость": "https://music.yandex.ru/album/32964463?utm_source=web&utm_medium=copy_link"
    },
    "Спортом": {
        "Спокойствие": "https://music.yandex.ru/artist/12428168?utm_medium=copy_link",
        "Стресс": "https://music.yandex.ru/users/yamusic-bestsongs/playlists/1908204?utm_medium=copy_link",
        "Радость": "https://music.yandex.ru/artist/21769054?utm_medium=copy_link"
    },
    "Отдохнуть": {
        "Спокойствие": "https://music.yandex.ru/artist/1081866?utm_medium=copy_link",
        "Стресс": "https://music.yandex.ru/artist/22937906?utm_medium=copy_link",
        "Радость": "https://music.yandex.ru/users/music-blog/playlists/1382?utm_medium=copy_link"
    }
}

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([["Учёбой", "Спортом", "Отдохнуть"]], one_time_keyboard=True)
    await update.message.reply_text("Привет! Чем собираешся заняться?", reply_markup=reply_markup)

async def handle_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = {"activity": update.message.text}
    reply_markup = ReplyKeyboardMarkup([["Спокойствие", "Стресс", "Радость"]], one_time_keyboard=True)
    await update.message.reply_text("Какое у тебя настроение?", reply_markup=reply_markup)

async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mood = update.message.text
    activity = user_state.get(user_id, {}).get("activity")

    if activity and mood in playlists.get(activity, {}):
        link = playlists[activity][mood]
        await update.message.reply_text(f"Вот музыка для тебя: {link}")
    else:
        await update.message.reply_text("Извини, я не смог найти подходящий плейлист.")

    user_state.pop(user_id, None)
    reply_markup = ReplyKeyboardMarkup([["Учёбой", "Спортом", "Отдохнуть"]], one_time_keyboard=True)
    await update.message.reply_text("Чем хочешь заняться?", reply_markup=reply_markup)

if __name__ == '__main__':
    TOKEN = os.getenv("8159054683:AAHCHzV6X3P2q9XdCA2iuV0MCSdXX18nwZM")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(Учёбой|Спортом|Отдохнуть)$"), handle_activity))
    app.add_handler(MessageHandler(filters.Regex("^(Спокойствие|Стресс|Радость)$"), handle_mood))

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()
