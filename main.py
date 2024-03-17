import telebot
import config
import emoji
from telebot import types

bot = config.bot


@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id not in config.user_state:
        # Устанавливаем начальное состояние для пользователя
        config.user_state[user_id] = {'started': True, 'language': None}
        change_language(message)  # Запускаем процесс выбора языка
    else:
        config.show_keyboard(message)
        handle_message(message)

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
    config.user_state[user_id]['language'] = lang_code  # Сохраняем выбранный язык

    if lang_code == 'en':
        bot.answer_callback_query(call.id, "English selected!")
    elif lang_code == 'ru':
        bot.answer_callback_query(call.id, "Русский выбран!")
    elif lang_code == 'ua':
        bot.answer_callback_query(call.id, "Українська вибрана!")

    bot.delete_message(call.message.chat.id, call.message.message_id)
    config.show_keyboard(user_id)  # Показываем клавиатуру после выбора языка





@bot.message_handler(func=lambda message: True)
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
            bot.send_message(user_id, {config.get_translation(user_lang, "account_message")})
            config.show_keyboard(user_id)
        elif message.text == settings_text:
            # Логика для кнопки "Настройки"
            bot.send_message(user_id, {config.get_translation(user_lang, "settings_message")})
            config.show_keyboard(user_id)
        elif message.text == tariffs_text:
            # Логика для кнопки "Тарифы"
            bot.send_message(user_id, {config.get_translation(user_lang, "tariffs_message")})
            config.show_keyboard(user_id)
        elif message.text == allow_models_text:
            # Логика для кнопки "Доступные модели"
            bot.send_message(user_id, {config.get_translation(user_lang, "models_message")})
            config.show_keyboard(user_id)
        else:
            bot.send_message(user_id, "Неизвестная команда.")
    else:
        # Если язык не выбран, запрашиваем его выбор
        change_language(message)



bot.infinity_polling()
