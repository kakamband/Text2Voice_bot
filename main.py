import telebot # підключення бібліотеки для роботи з Телеграм ботом
from gtts import gTTS # підключення бібліотеки для перетворення тексту в Аудіо


TOCKEN  = 'АPI-код, отриманий від BotFather'
usr_setting = {}


language = 'uk' # Стандартна мова обробки 
bot = telebot.TeleBot(TOCKEN) # Створення екземпляру бота 

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    global language # Створення доступу до загального налаштування мови
    if message.text == "/start": # Створення реакції бота на повідомлення "/start"
        keyboard = telebot.types.InlineKeyboardMarkup() # Створення шаблону клавіатури вибору мови 
        key_ru = telebot.types.InlineKeyboardButton(text = "Українська", callback_data = 'uk') # Формування кнопки "Українська"
        keyboard.add(key_ru) # Додавання кнопки "Українська" на шаблон клавіатури
        key_en = telebot.types.InlineKeyboardButton(text = "English", callback_data = 'en') # Формування кнопки "English"
        keyboard.add(key_en) # Додавання кнопки "English" на шаблон клавіатури
	# Повідомлення, що відправляється при старті бота
        bot.send_message(
		message.from_user.id,
		"Бот здатен перетворювати текст на аудіо. Вибери мову, після чого введи повідомлення для отримання результату",
		reply_markup = keyboard)

    else:
        tmp = gTTS(text = message.text, lang = usr_setting[str(message.chat.id)]) # використання бібліотеки для перетворення тексту з повідомлення на аудіо
        tmp.save('tmp.ogg') # Створення тимчасового файлу для запису отриманого аудіо
        audio = open('tmp.ogg', 'rb')
        bot.send_audio(message.from_user.id, audio) # Відправка готового аудіо у вигляді голосового повідомлення


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global language
    if call.data == "en": # Якщо виклик з кнопки буде "en", то мова зміниться на англійську
        usr_setting[str(call.message.chat.id)] = call.data
	# Відправка повідомлення про вдалу зміну мови
        bot.send_message(call.message.chat.id, "Мова обробки успішно змінена на англійську")
    elif call.data == "uk": # Якщо виклик з кнопки буде "uk", то мова зміниться на українську
        usr_setting[str(call.message.chat.id)] = call.data
	# Відправка повідомлення про вдалу зміну мови
        bot.send_message(call.message.chat.id, "Мова обробки успішно змінена на українську")
        

bot.polling(none_stop=True, interval=0) # Для безпереривного функціонування бота
