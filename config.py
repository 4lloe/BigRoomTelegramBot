import json
import telebot
import datetime
import anthropic
from telebot import types

telegrambot_token = "6981720034:AAFpPGkTreAt_WzUw65mPIxgMzdk4KJ2gV4"
api_key = "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"
anthropic.api_key = api_key
LOCALES_DIR = 'locales/'
bot = telebot.TeleBot(telegrambot_token)

# !!!Заменить на БД
# Создаем словарь для хранения языка каждого пользователя (в реальном проекте это стоит сохранять в базе данных)
user_state = {}


def user_init(user_id):  # Первая инициализация подписки FREE
    if user_id not in user_state:
        user_state[user_id] = {
            'started': True,
            'language': None,  # Установка языка по умолчанию, если необходимо
            'subscribe_type': 'Free',  # Установка начального типа подписки
            'valid_until': datetime.date(2024, 3, 19),  # Примерная дата окончания подписки
            'current_model': 'Default Model',  # Текущая модель
            'haiku_req': 0,  # Счётчик запросов хайку
            'sonnet_req': 0,  # Счётчик запросов соннетов
            'gptTurbo_req': 0,  # Счетчик запросов GPT-Turbo
            'payment_type': 'none'
        }

def load_translations(lang_code):
    with open(f'locales/{lang_code}.json', 'r', encoding='utf-8') as file:
        return json.load(file)


translations_cache = {}


def get_translation(lang_code, key):
    # Проверяем, загружены ли переводы для языка в кэш
    if lang_code not in translations_cache:
        translations_cache[lang_code] = load_translations(lang_code)
    # Получаем перевод по ключу
    return translations_cache[lang_code].get(key, "")


def get_user_language(user_id):
    if user_id in user_state:
        return user_state[user_id]
    else:
        return 'en'


def get_user_lang(user_id):
    if user_state[user_id]['language'] is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('English', callback_data='lang_en'))
        markup.add(types.InlineKeyboardButton('Russian', callback_data='lang_ru'))
        markup.add(types.InlineKeyboardButton('Ukrainian', callback_data='lang_ua'))
        bot.send_message(user_id, 'Choose language:', reply_markup=markup)
    else:
        show_keyboard(user_id)


# Метод реализующий вывод кастомной клавиатуры с опциями
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


# Функция создания InlineKeyboard для account
def get_account_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    # Получаем переводы для кнопок
    settings_text = get_translation(user_lang, "settings_btn")
    buy_premium_text = get_translation(user_lang, "buy_subscribe_btn")

    # Создаем инлайн клавиатуру
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⚙️" + settings_text, callback_data='settings'))
    markup.add(types.InlineKeyboardButton(text="🌠" + buy_premium_text, callback_data='buy_subscribe'))

    return markup


# Функция создания InlineKeyboard для /settings
def get_settings_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    voice_text = get_translation(user_lang, "sb_voice_answers_btn")
    creativity_text = get_translation(user_lang, "sb_answers_creativity_btn")
    language_change_text = get_translation(user_lang, "sb_language_change_btn")
    close_text = get_translation(user_lang, "close_btn")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🎨" + creativity_text, callback_data='creativity_settings'))
    markup.add(types.InlineKeyboardButton(text="🇺🇦" + language_change_text, callback_data='language_settings'))
    markup.add(types.InlineKeyboardButton(text=close_text, callback_data='close_callback'))

    return markup


# Функция создания InlineKeyboard для /subscribe
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

#Функция создания InlineKeyboard для /models
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

#Функция создания InlineKeyboard для первого сообщения после инициации /start
def get_preview_inline_keyboard(user_id):
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

    return markup


