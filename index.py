import os
import config
import stihoplet
from stihoplet import db
import telebot


sql = db.cursor()
bot = telebot.TeleBot(config.params['token'])

def userSetup (msg):
    start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
    start_keyboard.row('Стих, ёпта' , 'Настройки')
    bot.send_message(msg.chat.id, f'Здравствуйте, {msg.from_user.first_name}', reply_markup = start_keyboard)
    if sql.execute("SELECT id FROM users WHERE id = ?", (msg.from_user.id, )).fetchone() == None:
        sql.execute("INSERT INTO users (id, rhyme, str_count, stepSize, stressSyll) VALUES (?, ?, ?, ?, ?)", (msg.from_user.id, config.default['rhyme'], config.default['str_count'], config.default['stepSize'], config.default['stressSyll']))
        db.commit()

@bot.message_handler(commands=['start'])
def start(msg):
    userSetup(msg)
@bot.message_handler(commands=['report'])
def report(msg):
    bot.send_message(msg.chat.id, 'Чтобы донести на бараша напишите этому замечательному человеку!')
    bot.send_message(msg.chat.id, '@yusker0')

@bot.message_handler(commands=['delete_mp3'])
def delete_mp3(msg):
    if msg.from_user.username in config.admins:
        bot.send_message(msg.chat.id, 'Deleted')
        for file in os.listdir('audio'):
            os.remove(f'audio/{file}')
    else:
        bot.send_message(msg.chat.id, 'You have no rights to do this, Untermensch!')

@bot.message_handler(commands=['alert'])
def echo(msg):
    if msg.from_user.username in config.admins:
        for chat_id in sql.execute("SELECT id FROM users"):
            bot.send_message(chat_id, ' '.join(msg.text.split(' ')[1::]))
    else:
        bot.send_message(msg.chat.id, 'You have no rights to do this, Untermensch!')


@bot.message_handler(content_types=['text'])
def send_text(msg):
    msg_low = msg.text.lower()
    if msg_low == 'привет':
        bot.send_message(msg.chat.id, 'Опять пришлo, зочем?!')
    elif msg_low == 'пока':
        bot.send_message(msg.chat.id, 'Ну и вали отсюда!')
    elif msg_low == 'настройки':
        settings_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        settings_keyboard.row('Стихотворный размер:' , 'Рифмовка:', 'Кол-во строк:')
        settings_keyboard.row('Назад')
        set = sql.execute("SELECT stepSize, stressSyll, rhyme, str_count FROM users WHERE id = ?", (msg.from_user.id, )).fetchone()
        if set == None:
            userSetup(msg)
            set = sql.execute("SELECT stepSize, stressSyll, rhyme, str_count FROM users WHERE id = ?", (msg.from_user.id, )).fetchone()
        bot.send_message(msg.chat.id, f"Стихотворный размер: {config.beautySettings[str(set[0]) + str(set[1])]}\nРифмовка: {config.beautySettings[set[2]]}\nКол-во строк: {set[3]}\n", reply_markup = settings_keyboard)
    elif msg_low == 'рифмовка:':
        set = sql.execute("SELECT id FROM users WHERE id = ?", (msg.from_user.id, ))
        if set == None:
            userSetup(msg)
        rhyme_markup = telebot.types.InlineKeyboardMarkup()
        rhyme_markup.add(telebot.types.InlineKeyboardButton(text='Парная', callback_data='para'))
        rhyme_markup.add(telebot.types.InlineKeyboardButton(text='Перекрёстная', callback_data='perek'))
        rhyme_markup.add(telebot.types.InlineKeyboardButton(text='Кольцевая', callback_data='kolco'))
        bot.send_message(msg.chat.id, 'Рифмовка: ', reply_markup = rhyme_markup)
    elif msg_low == 'стихотворный размер:':
        set = sql.execute("SELECT id FROM users WHERE id = ?", (msg.from_user.id, ))
        if set == None:
            userSetup(msg)
        step_markup = telebot.types.InlineKeyboardMarkup()
        step_markup.add(telebot.types.InlineKeyboardButton(text='Ямб', callback_data = '2 1'))
        step_markup.add(telebot.types.InlineKeyboardButton(text='Хорей', callback_data = '2 2'))
        step_markup.add(telebot.types.InlineKeyboardButton(text='Дактиль', callback_data = '3 1'))
        step_markup.add(telebot.types.InlineKeyboardButton(text='Амфибрахий', callback_data = '3 2'))
        step_markup.add(telebot.types.InlineKeyboardButton(text='Анапест', callback_data = '3 3'))
        bot.send_message(msg.chat.id, 'Cтихотворный размер:', reply_markup = step_markup)
    elif msg_low == 'кол-во строк:':
        set = sql.execute("SELECT id FROM users WHERE id = ?", (msg.from_user.id, ))
        if set == None:
            userSetup(msg)
        str_markup = telebot.types.InlineKeyboardMarkup()
        str_markup.add(telebot.types.InlineKeyboardButton(text='16', callback_data = '16'))
        str_markup.add(telebot.types.InlineKeyboardButton(text='32', callback_data = '32'))
        str_markup.add(telebot.types.InlineKeyboardButton(text='64', callback_data = '64'))
        bot.send_message(msg.chat.id, 'Количество строк:', reply_markup = str_markup)
    elif msg_low == 'назад':
        start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        start_keyboard.row('Стих, ёпта' , 'Настройки')
        set = sql.execute("SELECT stepSize, stressSyll, rhyme, str_count FROM users WHERE id = ?", (msg.from_user.id, )).fetchone()
        if set == None:
            userSetup(msg)
            set = sql.execute("SELECT stepSize, stressSyll, rhyme, str_count FROM users WHERE id = ?", (msg.from_user.id, )).fetchone()
        bot.send_message(msg.chat.id, f"Стихотворный размер: {config.beautySettings[str(set[0]) + str(set[1])]}\nРифмовка: {config.beautySettings[set[2]]}\nКол-во строк: {set[3]}\n", reply_markup = start_keyboard)
    elif msg_low == 'стих, ёпта':
        msg_id = bot.send_message(msg.chat.id, "Подождите чуть-чуть!", reply_markup = telebot.types.ReplyKeyboardRemove(True)).message_id
        start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        start_keyboard.row('Стих, ёпта' , 'Настройки')
        set = sql.execute("SELECT stepSize, stressSyll, rhyme, str_count FROM users WHERE id = ?", (msg.from_user.id, )).fetchone()
        if set == None:
            userSetup(msg)
            set = sql.execute("SELECT stepSize, stressSyll, rhyme, str_count FROM users WHERE id = ?", (msg.from_user.id, )).fetchone()
        poem = stihoplet.stihoplet(set[0], set[1], set[2], set[3], msg.id)
        print(f'poem++ {msg.from_user.id}')
        bot.delete_message(msg.chat.id, msg_id)
        bot.send_message(msg.chat.id, poem['text'], reply_markup = start_keyboard)
        bot.send_audio(msg.chat.id, poem['audio'])
        os.remove(f'audio/{msg.id}.wav')
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data in ['2 1', '2 2', '3 1', '3 2', '3 3']:
        set = [int(call.data[0]), int(call.data[2])]
        sql.execute('UPDATE users SET stepSize = ?, stressSyll = ? WHERE id = ?', (set[0], set[1], call.message.chat.id))
        db.commit()
        bot.edit_message_text(config.beautySettings[str(set[0])+str(set[1])], call.message.chat.id, call.message.message_id, reply_markup = None)
    elif call.data in ['para', 'perek', 'kolco']:
        sql.execute('UPDATE users SET rhyme = ? WHERE id = ?', (call.data, call.message.chat.id))
        bot.edit_message_text(config.beautySettings[call.data], call.message.chat.id, call.message.message_id, reply_markup = None)
        db.commit()
    elif call.data in ['16', '32', '64']:
        sql.execute('UPDATE users SET str_count = ? WHERE id = ?', (int(call.data), call.message.chat.id))
        bot.edit_message_text(call.data, call.message.chat.id, call.message.message_id, reply_markup = None)
        db.commit()
    else:
        raise TypeError('Как?')
bot.polling()
