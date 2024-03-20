import telebot
import config
import emoji
from telebot import types

bot = config.bot

#Функция реализующая отклик на команду /start вступительной коанды
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    config.user_init(user_id)
    if user_id not in config.user_state:
        # Устанавливаем начальное состояние для пользователя
        change_language(message)  # Запускаем процесс выбора языка
    else:
        user_lang = config.user_state[user_id].get('language')
        if not user_lang:  # Проверяем, установил ли пользователь язык
            change_language(message)  # Если нет, запускаем процесс выбора языка
        else:
            welcome_message = config.get_translation(user_lang, "welcome_message")
            config.show_keyboard(user_id, welcome_message)
            handle_message(message)

#Функция реализующая отклик на команду /languag для установки языка пользователя
@bot.message_handler(commands=['language'])
def change_language(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
    markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
    markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
    bot.send_message(user_id, 'Choose language:', reply_markup=markup)

#Функция реализующая отклик на команду /settings для вывода меню настроек
@bot.message_handler(commands=['settings'])
def show_settings(message):
    user_id = message.from_user.id
    user_lang = config.user_state[user_id]['language']
    settings_text = "⚙️" + config.get_translation(user_lang, "settings_text")
    bot.send_message(user_id, settings_text, reply_markup=config.get_settings_inline_keyboard(user_id))

#Функция реализующая отклик на команду /subscribe для вывода доступных тарифов
@bot.message_handler(commands=['subscribe'])
def show_subscribe(message):
    user_id = message.from_user.id
    user_lang = config.user_state[user_id]['language']
    config.subscribe_text(message)


#Функция установки языка и вывода виджета выбраного языка
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    user_id = call.from_user.id
    lang_code = call.data.split('_')[1]

    if user_id not in config.user_state:
        config.user_state[user_id] = {'language': None}
    config.user_state[user_id]['language'] = lang_code# Сохраняем выбранный язык

    if lang_code == 'en':
        bot.answer_callback_query(call.id, "English selected!")
    elif lang_code == 'ru':
        bot.answer_callback_query(call.id, "Русский выбран!")
    elif lang_code == 'ua':
        bot.answer_callback_query(call.id, "Українська вибрана!")

    bot.delete_message(call.message.chat.id, call.message.message_id)
    user_lang = config.user_state[user_id]['language']
    welcome_message = config.get_translation(user_lang, "welcome_message")
    config.show_keyboard(user_id, welcome_message)


#Функция реагирования на нажатия клавиш главной клавиатуры
@bot.message_handler(func= lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_lang = config.user_state[user_id].get('language') if user_id in config.user_state else None

    if user_lang:
        user_lang = config.user_state[user_id]['language']
        account_text = config.get_translation(user_lang, "account_btn")
        settings_text = config.get_translation(user_lang, "settings_btn")
        tariffs_text = config.get_translation(user_lang, "tariffs_btn")
        allow_models_text = config.get_translation(user_lang, "allow_models_btn")

        # Проверяем текст сообщения и выполняем соответствующее действие
        if message.text == account_text:
            config.show_account(user_id)
        elif message.text == settings_text:
            show_settings(message)
        elif message.text == tariffs_text:
            show_subscribe(message)
        elif message.text == allow_models_text:
            config.model_description(message)
    else:
        # Если язык не выбран, запрашиваем его выбор
        change_language(message)

#Функция ответа на нажатие кнопки Аккаунт->Купить подписку
@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def callback_settings(message):
    show_settings(message)

#Функция ответа на нажатие кнопки Аккаунт->Подписка
@bot.callback_query_handler(func=lambda call: call.data == 'buy_subscribe')
def callback_subscribe(message):
    show_subscribe(message)

#Функция ответа на нажатие кнопки Настройки->Голосовые ответы
@bot.callback_query_handler(func=lambda call: call.data == 'voice_settings')
def callback_voice_settings(call):
    user_id = call.from_user.id
    user_lang = config.user_state[user_id]['language']
    message_text = config.get_translation(user_lang, "voice_settings_selected")
    bot.send_message(user_id, message_text)

#Функция ответа на нажатие кнопки Настройки->креативность ответов
@bot.callback_query_handler(func=lambda call: call.data == 'creativity_settings')
def callback_creativity_settings(call):
    user_id = call.from_user.id
    user_lang = config.user_state[user_id]['language']

@bot.callback_query_handler(func=lambda call: call.data == 'language_settings')
def callback_language_settings(call):
    change_language(call.from_user)

#Функция ответа на нажатие кнопки Настройки->Закрыть
@bot.callback_query_handler(func=lambda call: call.data == 'close_callback')
def callback_close_settings(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)


bot.infinity_polling()
