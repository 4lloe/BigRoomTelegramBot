import telebot
import config
import emoji
from telebot import types

bot = telebot.TeleBot(config.telegrambot_token)

# Инициализируем состояние каждого пользователя
config.user_states = {}  # {user_id: {'started': False, 'language': None}}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id not in config.user_states:
        # Устанавливаем начальное состояние для пользователя
        config.user_states[user_id] = {'started': True, 'language': None}
        change_language(message)  # Запускаем процесс выбора языка
    else:
        # Пользователь уже запустил бота и выбрал язык, выводим клавиатуру
        show_keyboard(message)

@bot.message_handler(commands=['language'])
def change_language(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
    markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
    markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
    bot.send_message(user_id, 'Choose language:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    user_id = call.from_user.id
    lang_code = call.data.split('_')[1]
    config.user_states[user_id]['language'] = lang_code  # Сохраняем выбранный язык

    if lang_code == 'en':
        bot.answer_callback_query(call.id, "English selected!")
    elif lang_code == 'ru':
        bot.answer_callback_query(call.id, "Русский выбран!")
    elif lang_code == 'ua':
        bot.answer_callback_query(call.id, "Українська вибрана!")

    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_keyboard(user_id)  # Показываем клавиатуру после выбора языка

def get_user_lang(user_id):

    if config.user_states[user_id]['language'] is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
        markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
        markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
        bot.send_message(user_id, 'Choose language:', reply_markup=markup)
    else:
        show_keyboard(user_id)

def show_keyboard(user_id):
    if user_id in config.user_states and config.user_states[user_id]['language']:
        user_lang = config.user_states[user_id]['language']
        welcome_message = config.get_translation(user_lang, "welcome_message")
        account_btn = config.get_translation(user_lang, "account_btn")
        settings_btn = config.get_translation(user_lang, "settings_btn")
        tariffs_btn = config.get_translation(user_lang, "tariffs_btn")
        allow_models_btn = config.get_translation(user_lang, "allow_models_btn")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(account_btn, settings_btn, allow_models_btn, tariffs_btn)

        bot.send_message(user_id, welcome_message, reply_markup=markup)

    else:
        get_user_lang(user_id)

def on_click(message):
    # Получаем user_id из сообщения
    user_id = message.from_user.id
    # Проверяем, что пользователь выбрал язык
    if user_id in config.user_states and config.user_states[user_id]['language']:
        # Получаем выбранный пользователем язык
        user_lang = config.user_states[user_id]['language']
        # Текст сообщения
        command_text = message.text

        # Словарь команд и их переводов
        commands = {
            'account_btn': config.get_translation(user_lang, "account_btn"),
            'settings_btn': config.get_translation(user_lang, "settings_btn"),
            'tariffs_btn': config.get_translation(user_lang, "tariffs_btn"),
            'allow_models_btn': config.get_translation(user_lang, "allow_models_btn")
        }

        # Проверяем, какая кнопка была нажата и выполняем соответствующие действия
        if command_text == commands['account_btn']:
            # Здесь логика для команды "account_btn"
            pass
        elif command_text == commands['settings_btn']:
            pass
        elif command_text == commands['tariffs_btn']:
            # Здесь логика для команды "tariffs_btn"
            pass
        elif command_text == commands['allow_models_btn']:
            # Здесь логика для команды "allow_models_btn"
            pass
        else:
            # Если нажатая кнопка не соответствует ни одной из команд
            bot.send_message(user_id, config.get_translation(user_lang, "unknown_command"))
    else:
        get_user_lang(user_id)

bot.infinity_polling()
