import telebot
from telebot import types
import data_handler
import config
from data_handler import SQLighter
import telegram

bot = telebot.TeleBot(config.token)
SQLighter = SQLighter(config.database_name)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет! 🎧️\n"
                     "Это крутой музыкальный бот, который поможет Вам найти лучшие хиты!\n"
                     "Что я умею?\n"
                     "/button - функция, позволяющая открыть меню\n")

    username = message.from_user.username
    user_id = message.from_user.id
    country = 0
    if message.from_user.language_code == 'ru':
        country = 1
    print(user_id)
    SQLighter.insert_user_id(username, user_id, country)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Топ-3 трека")
    item2 = types.KeyboardButton("Поиск по названию трека")
    item3 = types.KeyboardButton("Жанр")
    item4 = types.KeyboardButton("Топ-3 исполнителя")
    item5 = types.KeyboardButton("Топ-3 альбома")
    #item6 = types.KeyboardButton(SQLighter.get_genre())

    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    flag_genre = 0
    genres = ['Pop', 'K-Pop', 'Hip-hop', 'R&B', 'Rock', 'Детская музыка', 'Русский рэп']

    if message.text == "Топ-3 трека":
        bot.send_message(message.chat.id, 'Можете увидеть топ-3 трека по Вашей стране:\n')
        if message.from_user.language_code == 'ru':
            country = 1
        top_3 = SQLighter.get_top_3(country)
        for i in top_3:
            print(i)
            bot.send_message(message.chat.id, '🎵 ' + str(i[1]) + ' - ' + str(i[2]) + '\n' + str(i[3]))
        button_message(message)

    elif message.text == "Поиск по названию трека":
        flag_get_track_by_name = 1
        bot.send_message(message.chat.id, 'Можете начать поиск песен по названию:\n')

    elif message.text == "Жанр":
        flag_genre = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        genre = str(SQLighter.get_genre())

        for i in range(len(genres)):
            ind_genre = str(genre).find(genres[i])
            item_i = types.KeyboardButton(genre[ind_genre:ind_genre + len(genres[i])])
            #print(genre[ind_genre:ind_genre + len(genres[i])])
            markup.add(item_i)
        bot.send_message(message.chat.id, 'Можете начать поиск песен по жанру:\n', reply_markup=markup)

    elif message.text in genres:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        track = SQLighter.get_track_by_genre(message.text)
        for i in track:
            print(i)
            bot.send_message(message.chat.id, '🎵 ' + str(i[0]) + ' - ' + str(i[1]) + '\n' + str(i[2]), reply_markup=markup)
        button_message(message)

    elif message.text == "Топ-3 исполнителя":
        bot.send_message(message.chat.id, 'Можете увидеть топ-3 исполнителя по Вашей стране:\n')
        if message.from_user.language_code == 'ru':
            country = 1
        top_3_artists = SQLighter.get_top_3_artists(country)
        for i in top_3_artists:
            print(i)
            bot.send_message(message.chat.id, '🎤 ' + str(i[2]))
        button_message(message)

    elif message.text == "Топ-3 альбома":
        bot.send_message(message.chat.id, 'Можете увидеть топ-3 альбома по Вашей стране:\n')
        if message.from_user.language_code == 'ru':
            country = 1
        top_3_albums = SQLighter.get_top_3_albums(country)
        #bot.send_message(message.chat.id, top_3_albums)
        for i in top_3_albums:
            bot.send_message(message.chat.id, '💿 ' + str(i)[2:-3])
        button_message(message)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        track_name = message.text
        ind = 0
        track_and_performer = SQLighter.get_track_by_name(track_name)
        track_id = SQLighter.return_track_id(track_name)
        #print(track_id)

        for t in track_and_performer:
            bot.send_message(message.chat.id, '🎵 ' + str(t[0]) + ' - ' + str(t[1]) + '\n' + str(t[2]), reply_markup=markup)
            if message.chat.id != '':
                ind += 1
        if ind == 0:
            bot.send_message(message.chat.id, 'Нет такой песни🤬! Проверьте корректность ввода.', reply_markup=markup)
        for id_ in track_id:
            id_ = str(id_)
            SQLighter.insert_playlist(id_[1:-2], message.from_user.id)

bot.infinity_polling()
