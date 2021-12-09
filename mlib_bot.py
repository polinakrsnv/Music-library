import telebot
from telebot import types
import data_handler
import config
from data_handler import SQLighter


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет! 🎧️\n"
                     "Это крутой музыкальный бот, который поможет Вам найти лучшие хиты!\n"
                     "Что я умею?\n"
                     "/button - функция, позволяющая открыть меню\n")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Топ-3")
    item2 = types.KeyboardButton("Песня")
    item3 = types.KeyboardButton("Жанр")
    item4 = types.KeyboardButton("Исполнитель")
    item5 = types.KeyboardButton("Альбом")
    #item6 = types.KeyboardButton(SQLighter.get_genre())

    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Топ-3":
        bot.send_message(message.chat.id, 'Можете увидеть топ-3 прослушиваний по Вашей стране:\n')

    elif message.text == "Песня":
        bot.send_message(message.chat.id, 'Можете начать поиск песен по названию:\n')

    elif message.text == "Жанр":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        genre = SQLighter(config.database_name).get_genre()
        item1 = types.KeyboardButton(str(genre))
        markup.add(item1)
        bot.send_message(message.chat.id, 'Можете начать поиск песен по жанру:\n', reply_markup=markup)
        #bot.send_message(message.chat.id, genre)

    elif message.text == "Исполнитель":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2 = types.KeyboardButton("тут надо как-то ввести исполнителя")
        markup.add(item2)
        bot.send_message(message.chat.id, 'Можете начать поиск песен по исполнителю:\n', reply_markup=markup)

    elif message.text == "Альбом":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item3 = types.KeyboardButton("тут вводим альбом")
        markup.add(item3)
        bot.send_message(message.chat.id, 'Можете начать поиск песен по альбому:\n', reply_markup=markup)


bot.infinity_polling()
