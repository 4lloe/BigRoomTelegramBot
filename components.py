import json
import datetime

# Импорт модулей для работы с Telegram API
import interactions  # Пользовательский модуль, возможно, для взаимодействия с ботом
from utils.config import bot  # Импорт конфигурации бота
from telebot import types  # Импорт типов клавиатур для Telegram
import os  # Импорт модуля для работы с операционной системой

# Создание и инициализация словаря для хранения состояния пользователей
user_state = {}
# Создание списка для хранения контекста пользователей
user_context = []


# Функция инициализации пользователя при первом входе
def user_init(user_id):
    if user_id not in user_state:
        user_state[user_id] = {
            'started': True,  # Флаг первого запуска
            'language': None,  # Язык пользователя
            'subscribe_type': 'gpt-3.5-turbo-instruct',  # Тип подписки
            'valid_until': datetime.date(2024, 3, 19),  # Дата окончания подписки
            'assistant_role': "No role for now",  # Роль ассистента
            'haiku_req': 3,  # Счетчик запросов хайку
            'sonnet_req': 0,  # Счетчик запросов сонетов
            'gptTurbo_req': 0,  # Счетчик запросов GPT-Turbo
            'payment_type': 'none'  # Тип оплаты
        }


# Загрузка переводов из файла JSON
def load_translations(lang_code):
    with open(f'locales/{lang_code}.json', 'r', encoding='utf-8') as file:
        return json.load(file)


# Кэш для хранения загруженных переводов
translations_cache = {}


# Получение перевода по ключу и языковому коду
def get_translation(lang_code, key):
    # Проверка, есть ли переводы для данного языка в кэше
    if lang_code not in translations_cache:
        translations_cache[lang_code] = load_translations(lang_code)
    # Получение перевода по ключу
    return translations_cache[lang_code].get(key, "")


# Получение языка пользователя по его ID
def get_user_language(user_id):
    if user_id in user_state:
        return user_state[user_id]
    else:
        return 'en'


# Отправка клавиатуры для выбора языка
def get_user_lang(user_id):
    if user_state[user_id]['language'] is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
        markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
        markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
        bot.send_message(user_id, 'Choose language:', reply_markup=markup)
    else:
        show_keyboard(user_id)


# Отображение кастомной клавиатуры с опциями
def show_keyboard(user_id, call):
    if user_id in user_state and user_state[user_id]['language']:
        user_lang = user_state[user_id]['language']
        account_btn = get_translation(user_lang, "account_btn")
        settings_btn = get_translation(user_lang, "settings_btn")
        tariffs_btn = get_translation(user_lang, "tariffs_btn")
        allow_models_btn = get_translation(user_lang, "allow_models_btn")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        markup.add(account_btn, settings_btn, allow_models_btn, tariffs_btn)

        bot.send_message(user_id, call, reply_markup=markup)

    else:
        get_user_lang(user_id)


# Функция создания InlineKeyboard для раздела "Account"
def get_account_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    # Получение переводов для кнопок
    settings_text = get_translation(user_lang, "settings_btn")
    buy_premium_text = get_translation(user_lang, "buy_subscribe_btn")

    # Создание инлайн клавиатуры
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⚙️" + settings_text, callback_data='settings'))
    markup.add(types.InlineKeyboardButton(text="🌠" + buy_premium_text, callback_data='buy_subscribe'))

    return markup


# Функция создания InlineKeyboard для раздела "/settings"
def get_settings_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    language_change_text = get_translation(user_lang, "sb_language_change_btn")
    choose_models_text = get_translation(user_lang, "choose_model_settings_text")
    close_text = get_translation(user_lang, "close_btn")
    ai_model_text = get_translation(user_lang, "ai_model_btn")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🇺🇦" + language_change_text, callback_data='language_settings'))
    markup.add(types.InlineKeyboardButton(text="👾" + choose_models_text, callback_data='models_settings'))
    markup.add(types.InlineKeyboardButton(text="🤖" + ai_model_text, callback_data='choose_ai_call-handler'))
    markup.add(types.InlineKeyboardButton(text=close_text, callback_data='close_callback'))

    return markup


# Функция создания InlineKeyboard для раздела "/subscribe"
def get_subscribe_inline_keyboard(user_id):
    global starter_text, intermediate_text, advanced_text
    user_lang = user_state[user_id]['language']
    close_btn = get_translation(user_lang, "close_btn")
    if user_lang == "en":
        starter_text = "👌 Buy Starter for 14.80$/month"
        intermediate_text = "🌉 Buy Intermediate for 19.93$/month"
        advanced_text = "🚀 Buy Advancedfor 29.93$/month"
    elif user_lang == "ru":
        starter_text = "👌 Купить Starter за 14.80$/месяц"
        intermediate_text = "🌉 Купить Intermediate за 19.93$/месяц"
        advanced_text = "🚀 Купить Advanced за 29.93$/месяц"
    elif user_lang == "ua":
        starter_text = "👌 Купити Starter за 14.80$/місяць"
        intermediate_text = "🌉 Купити Intermediate за 19.93$/місяць"
        advanced_text = "🚀 Купити Advanced за 29.93$/місяць"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=starter_text, callback_data='starter_callback'))
    markup.add(types.InlineKeyboardButton(text=intermediate_text, callback_data='intermediate'))
    markup.add(types.InlineKeyboardButton(text=advanced_text, callback_data='advanced_callback'))
    markup.add(types.InlineKeyboardButton(text=close_btn, callback_data='close_callback'))

    return markup


# Функция создания InlineKeyboard для раздела "/models"
def get_models_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']
    marketer = get_translation(user_lang, 'marketer_btn')
    programmer = get_translation(user_lang, 'programmer_btn')
    trader = get_translation(user_lang, 'trader_btn')
    close_btn = get_translation(user_lang, "close_btn")
    subscribe = get_translation(user_lang, 'tariffs_btn')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="📝 " + marketer, callback_data='marketer_callback'))
    markup.add(types.InlineKeyboardButton(text="💻 " + programmer, callback_data='programmer_callback'))
    markup.add(types.InlineKeyboardButton(text="💹 " + trader, callback_data='trader_callback'))
    markup.add(types.InlineKeyboardButton(text="🚀 " + subscribe, callback_data='subscribe_callback'))
    markup.add(types.InlineKeyboardButton(text=close_btn, callback_data='close_callback'))

    return markup


# Функция создания InlineKeyboard для первого сообщения после инициации /start
def get_preview_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']
    marketer = get_translation(user_lang, 'marketer_btn')
    programmer = get_translation(user_lang, 'programmer_btn')
    trader = get_translation(user_lang, 'trader_btn')
    clean_chat = get_translation(user_lang, 'clean_chat_msg')
    subscribe = get_translation(user_lang, 'tariffs_btn')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="📝 " + marketer, callback_data='marketer_callback'))
    markup.add(types.InlineKeyboardButton(text="💻 " + programmer, callback_data='programmer_callback'))
    markup.add(types.InlineKeyboardButton(text="💹 " + trader, callback_data='trader_callback'))
    markup.add(types.InlineKeyboardButton(text="💬" + clean_chat, callback_data='clean_chat'))
    markup.add(types.InlineKeyboardButton(text="🚀 " + subscribe, callback_data='subscribe_callback'))

    return markup


# Отправка пользователю клавиатуры выбора языка
def get_language_inline_k(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
    markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
    markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
    bot.send_message(user_id, 'Choose language:', reply_markup=markup)


# Отправка пользователю клавиатуры выбора искусственного интеллекта
def get_choose_ai_inline_k(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('☁️ Claude-3', callback_data='claude_inline_btn'))
    markup.add(types.InlineKeyboardButton('💻 Chat-GPT', callback_data='chat-gpt_inline_btn'))
    bot.send_message(user_id, interactions.show_select_ai_interaction(user_lang=user_state[user_id]['language']),
                     reply_markup=markup)


# Выбор языка пользователем
def choose_language(user_id):
    get_language_inline_k(user_id)


# Загрузка и конвертация документа
def download_and_convert_document(file_id, message):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_size = file_info.file_size

    # Проверка размера файла (не более 10 МБ)
    if file_size > 10 * 1024 * 1024:
        bot.send_message(message.chat.id, "The file is too large. Please upload a smaller file.")
        return

    # Сохранение файла локально
    with open('temp_file.pdf', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Конвертация PDF в текст
    text = convert_to_text('temp_file.pdf')

    # Отправка текста пользователю
    bot.send_message(message.chat.id, text)

    # Удаление временного файла
    os.remove('temp_file.pdf')


# Конвертация PDF в текст
def convert_to_text(inputPDF):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    import io

    # Использование PDFResourceManager для хранения ресурсов
    res_mgr = PDFResourceManager()
    ret_data = io.StringIO()
    txt_converter = TextConverter(res_mgr, ret_data, laparams=LAParams())
    interpreter = PDFPageInterpreter(res_mgr, txt_converter)

    # Открытие файла PDF
    with open(inputPDF, 'rb') as in_file:
        for page in PDFPage.get_pages(in_file, caching=True):
            interpreter.process_page(page)

    text = ret_data.getvalue()

    # Закрытие конвертера и возврат текста
    txt_converter.close()
    ret_data.close()
    return text


# Отправка сообщения об ошибке
def send_error_message(message):
    bot.send_message(message.chat.id, "Something wrong")
