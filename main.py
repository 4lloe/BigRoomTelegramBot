import telebot
from telebot import types

bot = telebot.TeleBot('6981720034:AAFpPGkTreAt_WzUw65mPIxgMzdk4KJ2gV4')
language = "english"
@bot.message_handler(commands=['start'])
def getUser_lang(message):
    bot.send_message(message.chat.id, 'Hello, im BigRoom tg bot, choose language to use')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English'))
    return language;

#equals  bot.polling(none_stop=True)
bot.infinity_polling()
