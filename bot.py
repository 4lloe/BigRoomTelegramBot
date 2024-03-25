import components
import interactions
from telebot import types

from utils.anthropic_utils import make_user_prompt
from utils.config import bot


# Функция реализующая отклик на команду /start вступительной коанды
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id not in components.user_state:
        components.user_init(user_id)
        change_language(message)
    else:
        user_lang = components.user_state[user_id].get('language')
        if not user_lang:
            change_language(message)
        else:
            welcome_message = components.get_translation(user_lang, "welcome_message")
            components.show_keyboard(user_id, welcome_message)
            bot.send_message(user_id, interactions.show_bot_preview(user_lang),
                             reply_markup=components.get_preview_inline_keyboard(user_id))


# Функция реализующая отклик на команду /language для установки языка пользователя
@bot.message_handler(commands=['language'])
def change_language(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
    markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
    markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
    bot.send_message(user_id, 'Choose language:', reply_markup=markup)


# Функция реализующая отклик на команду /settings для вывода меню настроек
@bot.message_handler(commands=['settings'])
def show_settings(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']
    settings_text = "⚙️" + components.get_translation(user_lang, "settings_text")
    bot.send_message(user_id, settings_text, reply_markup=components.get_settings_inline_keyboard(user_id))


# Функция реализующая отклик на команду /subscribe для вывода доступных тарифов
@bot.message_handler(commands=['subscribe'])
def show_subscribe(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']
    interactions.subscribe_text(message)


# Функция реализующая отклик команды смены языка
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    global language_selected
    user_id = call.from_user.id
    lang_code = call.data.split('_')[1]
    is_new_user = user_id not in components.user_state or components.user_state[user_id].get('language') is None

    if user_id not in components.user_state:
        components.user_state[user_id] = {'language': None}

    components.user_state[user_id]['language'] = lang_code
    user_lang = components.user_state[user_id]['language']

    if lang_code == 'en':
        bot.answer_callback_query(call.id, "English selected!")
        language_selected = "🇬🇧" + components.get_translation(user_lang, "language_selected")
    elif lang_code == 'ru':
        bot.answer_callback_query(call.id, "Русский выбран!")
        language_selected = "🇷🇺" + components.get_translation(user_lang, "language_selected")
    elif lang_code == 'ua':
        bot.answer_callback_query(call.id, "Українська вибрана!")
        language_selected = "🇺🇦" + components.get_translation(user_lang, "language_selected")

    if is_new_user:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        components.show_keyboard(user_id, language_selected)
        start_command(call)
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        components.show_keyboard(user_id, language_selected)


# Функция реагирования на нажатия клавиш главной клавиатуры
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id].get('language') if user_id in components.user_state else None

    if user_lang:
        user_lang = components.user_state[user_id]['language']
        account_text = components.get_translation(user_lang, "account_btn")
        settings_text = components.get_translation(user_lang, "settings_btn")
        tariffs_text = components.get_translation(user_lang, "tariffs_btn")
        allow_models_text = components.get_translation(user_lang, "allow_models_btn")

        # Проверяем текст сообщения и выполняем соответствующее действие
        if message.text == account_text:
            interactions.show_account(user_id)
        elif message.text == settings_text:
            show_settings(message)
        elif message.text == tariffs_text:
            show_subscribe(message)
        elif message.text == allow_models_text:
            interactions.model_description(message)
        else:
            make_user_prompt(message)
    else:
        # Если язык не выбран, запрашиваем его выбор
        change_language(message)


# Функция ответа на нажатие кнопки Аккаунт->Купить подписку
@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def callback_settings(message):
    show_settings(message)


# Функция ответа на нажатие кнопки Аккаунт->Подписка
@bot.callback_query_handler(func=lambda call: call.data == 'buy_subscribe')
def callback_subscribe(message):
    show_subscribe(message)


# Функция ответа на нажатие кнопки Настройки->Настройки языка
@bot.callback_query_handler(func=lambda call: call.data == 'language_settings')
def callback_language_settings(call):
    change_language(call)


# Функция ответа на нажатие кнопки Настройки->Закрыть
@bot.callback_query_handler(func=lambda call: call.data == 'close_callback')
def callback_close_settings(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Функция ответа на нажатие кнопки Подписка
@bot.callback_query_handler(func=lambda call: call.data == 'subscribe_callback')
def subscribe_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_subscribe(call)


# Функция ответа на нажатие кнопки Модели->Маркетолог
@bot.callback_query_handler(func=lambda call: call.data == 'marketer_callback')
def marketer_callback(call):
    user_id = call.from_user.id
    user_lang = components.user_state[user_id].get('language', 'en')  # Значение по умолчанию - английский
    description = interactions.marketer_model_description(user_lang)
    bot.send_message(user_id, description)


# Функция ответа на нажатие кнопки Модели->Програмист
@bot.callback_query_handler(func=lambda call: call.data == 'programmer_callback')
def programmer_callback(call):
    user_id = call.from_user.id
    user_lang = components.user_state[user_id].get('language', 'en')  # Значение по умолчанию - английский
    description = interactions.programmer_model_description(user_lang)
    bot.send_message(user_id, description)


# Функция ответа на нажатие кнопки Модели->Трейдер
@bot.callback_query_handler(func=lambda call: call.data == 'trader_callback')
def trader_callback(call):
    user_id = call.from_user.id
    user_lang = components.user_state[user_id].get('language', 'en')  # Значение по умолчанию - английский
    description = interactions.trader_model_description(user_lang)
    bot.send_message(user_id, description)


bot.infinity_polling()
