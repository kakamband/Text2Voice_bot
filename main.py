import telebot
from gtts import gTTS


TOCKEN  = '*'

language = 'ru'
bot = telebot.TeleBot(TOCKEN)

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    global language
    if message.text == "/start":
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_ru = telebot.types.InlineKeyboardButton(text = "Русский", callback_data = 'ru')
        keyboard.add(key_ru)
        key_en = telebot.types.InlineKeyboardButton(text = "English", callback_data = 'en')
        keyboard.add(key_en)
        bot.send_message(message.from_user.id, "Ты написал СТАРТ", reply_markup = keyboard)
        print(language)

    else:
        tmp = gTTS(text = message.text, lang = language)
        tmp.save('tmp.ogg')
        audio = open('tmp.ogg', 'rb')
        bot.send_audio(message.from_user.id, audio)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global language
    if call.data == "en":
        language = call.data
        bot.send_message(call.message.chat.id, "Язык обработки успешно изменён на английский")
    elif call.data == "ru":
        call.data == "ru"
        language = call.data
        bot.send_message(call.message.chat.id, "Язык обработки успешно изменён на русский")
        

bot.polling(none_stop=True, interval=0)
