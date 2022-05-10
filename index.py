import os
import config
import stihoplet
import telebot
import pars

bot = telebot.TeleBot(config.params['token'])
@bot.message_handler(commands=['start'])
def start(msg):
    start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
    start_keyboard.row('Стих, ёпта' , 'Настройки')
    bot.send_message(msg.chat.id, f'Здравствуйте, {msg.from_user.first_name}', reply_markup = start_keyboard)
    if not os.path.exists(f'users/user{msg.from_user.id}'):
        f = open(f'users/user{msg.from_user.id}.sps', 'w')
        f.write(config.default['cens']+'\n'+config.default['rifm']+'\n'+str(config.default['str']))
        f.close()
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

@bot.message_handler(commands=['update_dicts'])
def update_dicts(msg):
    if msg.from_user.username in config.admins:
        pars.formal()
    else:
        bot.send_message(msg.chat.id, 'You have no rights to do this, Untermensch!')

@bot.message_handler(commands=['alert'])
def echo(msg):
    if msg.from_user.username in config.admins:
        for chat_id in os.listdir('users'):
            chat_id = ''.join(chat_id.split('.')[0][4::])
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
        settings_keyboard.row('Цензурность:' , 'Рифмовка:', 'Кол-во строк:')
        settings_keyboard.row('Назад')
        f = open(f'users/user{msg.from_user.id}.sps', 'r')
        set = f.read().split('\n')
        bot.send_message(msg.chat.id, f"Цензурность: {config.beautySettings[set[0]]}\nРифмовка: {config.beautySettings[set[1]]}\nКол-во строк: {set[2]}\n", reply_markup = settings_keyboard)
    elif msg_low == 'цензурность:':
        cens_markup = telebot.types.InlineKeyboardMarkup()
        cens_markup.add(telebot.types.InlineKeyboardButton(text='Цензурно', callback_data='cens'))
        cens_markup.add(telebot.types.InlineKeyboardButton(text='Нецензурно', callback_data='uncens'))
        bot.send_message(msg.chat.id, 'Цензурность: ', reply_markup = cens_markup)
    elif msg_low == 'рифмовка:':
        rifm_markup = telebot.types.InlineKeyboardMarkup()
        rifm_markup.add(telebot.types.InlineKeyboardButton(text='Парная', callback_data='para'))
        rifm_markup.add(telebot.types.InlineKeyboardButton(text='Перекрёстная', callback_data='perek'))
        rifm_markup.add(telebot.types.InlineKeyboardButton(text='Кольцевая', callback_data='kolco'))
        bot.send_message(msg.chat.id, 'Рифмовка:', reply_markup = rifm_markup)
    elif msg_low == 'кол-во строк:':
        str_markup = telebot.types.InlineKeyboardMarkup()
        str_markup.add(telebot.types.InlineKeyboardButton(text='16', callback_data = 16))
        str_markup.add(telebot.types.InlineKeyboardButton(text='32', callback_data = 32))
        str_markup.add(telebot.types.InlineKeyboardButton(text='64', callback_data = 64))
        bot.send_message(msg.chat.id, 'Количество строк:', reply_markup = str_markup)
    elif msg_low == 'назад':
        start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        start_keyboard.row('Стих, ёпта' , 'Настройки')
        f = open(f'users/user{msg.from_user.id}.sps', 'r')
        set = f.read().split('\n')
        bot.send_message(msg.chat.id, f"Цензурность: {config.beautySettings[set[0]]}\nРифмовка: {config.beautySettings[set[1]]}\nКол-во строк: {set[2]}\n", reply_markup = start_keyboard)
    elif msg_low == 'стих, ёпта':
        msg_id = bot.send_message(msg.chat.id, "Подождите чуть-чуть!", reply_markup = telebot.types.ReplyKeyboardRemove(True)).message_id
        print('++poem')
        start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        start_keyboard.row('Стих, ёпта' , 'Настройки')
        f = open(f'users/user{msg.from_user.id}.sps', 'r')
        set = f.read().split('\n')
        poem = stihoplet.stihoplet(config.params['lang'], set[0], set[1], int(set[2]), msg.id)
        print('poem++')
        bot.delete_message(msg.chat.id, msg_id)
        bot.send_message(msg.chat.id, poem['text'], reply_markup = start_keyboard)
        bot.send_audio(msg.chat.id, poem['audio'])
        os.remove(f'audio/{msg.id}.wav')
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data in ['cens', 'uncens']:
        f = open(f'users/user{call.message.chat.id}.sps', 'r')
        set = f.read().split('\n')
        f.close()
        f = open(f'users/user{call.message.chat.id}.sps', 'w')
        f.write(f'{call.data}\n{set[1]}\n{set[2]}')
        bot.edit_message_text(config.beautySettings[call.data], call.message.chat.id, call.message.message_id, reply_markup = None)
    elif call.data in ['para', 'perek', 'kolco']:
        f = open(f'users/user{call.message.chat.id}.sps', 'r')
        set = f.read().split('\n')
        f.close()
        f = open(f'users/user{call.message.chat.id}.sps', 'w')
        f.write(f'{set[0]}\n{call.data}\n{set[2]}')
        bot.edit_message_text(config.beautySettings[call.data], call.message.chat.id, call.message.message_id, reply_markup = None)
    elif call.data in ['16', '32', '64']:
        f = open(f'users/user{call.message.chat.id}.sps', 'r')
        set = f.read().split('\n')
        f.close()
        f = open(f'users/user{call.message.chat.id}.sps', 'w')
        f.write(f'{set[0]}\n{set[1]}\n{call.data}')
        bot.edit_message_text(call.data, call.message.chat.id, call.message.message_id, reply_markup = None)
    else:
        raise TypeError('Как?')
bot.polling()