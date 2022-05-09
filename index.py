import os
import config
import stihoplet
import telebot

bot = telebot.TeleBot(config.params['token'])
@bot.message_handler(commands=['start'])
def start(msg):
    start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
    start_keyboard.row('Стих, ёпта' , 'Настройки')
    bot.send_message(msg.chat.id, f'Здравствуйте, {msg.from_user.first_name}', reply_markup = start_keyboard)
    if not os.path.exists(f'users/{msg.from_user.username}'):
        f = open(f'users/{msg.from_user.username}.sps', 'w')
        f.write(config.default['cens']+'\n'+config.default['rifm']+'\n'+str(config.default['str']))
        f.close()

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
        f = open(f'users/{msg.from_user.username}.sps', 'r')
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
        f = open(f'users/{msg.from_user.username}.sps', 'r')
        set = f.read().split('\n')
        bot.send_message(msg.chat.id, f"Цензурность: {config.beautySettings[set[0]]}\nРифмовка: {config.beautySettings[set[1]]}\nКол-во строк: {set[2]}\n", reply_markup = start_keyboard)
    elif msg_low == 'стих, ёпта':
        start_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        start_keyboard.row('Стих, ёпта' , 'Настройки')
        msg_id = bot.send_message(msg.chat.id, "Подождите чуть-чуть!", reply_markup = telebot.types.ReplyKeyboardRemove(True)).message_id
        f = open(f'users/{msg.from_user.username}.sps', 'r')
        set = f.read().split('\n')
        poem = stihoplet.stihoplet(config.params['lang'], set[0], set[1], int(set[2]))
        bot.delete_message(msg.chat.id, msg_id)
        bot.send_message(msg.chat.id, poem['text'], reply_markup = start_keyboard)
        bot.send_audio(msg.chat.id, poem['audio'])
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data in ['cens', 'uncens']:
        f = open(f'users/{call.message.chat.username}.sps', 'r')
        set = f.read().split('\n')
        f.close()
        os.remove(f'users/{call.message.chat.username}.sps')
        f = open(f'users/{call.message.chat.username}.sps', 'w')
        f.write(f'{call.data}\n{set[1]}\n{set[2]}')
        bot.edit_message_text(config.beautySettings[call.data], call.message.chat.id, call.message.message_id, reply_markup = None)
    elif call.data in ['para', 'perek', 'kolco']:
        f = open(f'users/{call.message.chat.username}.sps', 'r')
        set = f.read().split('\n')
        f.close()
        os.remove(f'users/{call.message.chat.username}.sps')
        f = open(f'users/{call.message.chat.username}.sps', 'w')
        f.write(f'{set[0]}\n{call.data}\n{set[2]}')
        bot.edit_message_text(config.beautySettings[call.data], call.message.chat.id, call.message.message_id, reply_markup = None)
    elif call.data in ['16', '32', '64']:
        f = open(f'users/{call.message.chat.username}.sps', 'r')
        set = f.read().split('\n')
        f.close()
        os.remove(f'users/{call.message.chat.username}.sps')
        f = open(f'users/{call.message.chat.username}.sps', 'w')
        f.write(f'{set[0]}\n{set[1]}\n{call.data}')
        bot.edit_message_text(call.data, call.message.chat.id, call.message.message_id, reply_markup = None)
    else:
        raise TypeError('Как?')




bot.polling()