import json
import telebot
import datetime
from telebot import types

telegrambot_token = "6981720034:AAFpPGkTreAt_WzUw65mPIxgMzdk4KJ2gV4"
language = "english"
LOCALES_DIR = 'locales/'
bot = telebot.TeleBot(telegrambot_token)

#!!!Заменить на БД
# Создаем словарь для хранения языка каждого пользователя (в реальном проекте это стоит сохранять в базе данных)
user_state = {}


def user_init(user_id): # Первая инициализация подписки FREE
    user_state[user_id] = {'started': True, 'language': None,'subscribe_type': "free",
                           'valid_until': datetime.date(0000, 00, 00), 'payment_type': 'none'}

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

#Метод реализующий информационое сообщение с Inline клавиатурой для опции Account
def show_account(user_id):
    user_lang = user_state[user_id]['language']
    subscribe_type = user_state[user_id].get('subscribe_type', 'Free')
    valid_until = user_state[user_id].get('valid_until', '-')
    cur_model = user_state[user_id].get('current_model', 'Claude Haiku Free')
    haiku_req = user_state[user_id].get('haiku_req', 2)
    sonnet_req = user_state[user_id].get('sonnet_req', 0)
    gpt_turbo_req = user_state[user_id].get('gptTurbo_req', 0)

    account_message_template = (
        f"👤 User ID: {user_id}\n"
        f"⭐️ Subscription Type: {subscribe_type}\n"
        f"📆 Valid Until: {valid_until}\n"
        f"🤖 Current model: {cur_model}\n"
        f"–––––––––––––––––––––––––––––\n"
        f"🌸 Haiku requests: {haiku_req}\n"
        f"📜 Sonnet requests: {sonnet_req}\n"
        f"💨 GPT-Turbo: {gpt_turbo_req}\n"
    )

    if user_lang == 'en':
        bot.send_message(user_id, account_message_template)
        bot.send_message(user_id, account_message_template, reply_markup=get_inline_keyboard(user_id))
    elif user_lang == 'ru':
        account_message_ru = (((((account_message_template.replace("Subscription Type", "Тип подписки")
                              .replace("Valid Until", "Действительно до"))
                              .replace("Current model", "Текущая модель"))
                              .replace("Haiku requests", "Запросы Хайку"))
                              .replace("Sonnet requests", "Запросы Сонетов"))
                              .replace("GPT-Turbo", "GPT-Турбо"))
        bot.send_message(user_id, account_message_ru)
        bot.send_message(user_id, account_message_template, reply_markup=get_inline_keyboard(user_id))
    elif user_lang == 'ua':
        account_message_ua = (((((account_message_template.replace("Subscription Type", "Тип підписки")
                              .replace("Valid Until", "Дійсно до"))
                              .replace("Current model", "Поточна модель"))
                              .replace("Haiku requests", "Запити Хайку"))
                              .replace("Sonnet requests", "Запити Сонетів"))
                              .replace("GPT-Turbo", "GPT-Турбо"))
        bot.send_message(user_id, account_message_ua)
        bot.send_message(user_id, account_message_template, reply_markup=get_inline_keyboard(user_id))
    else:
        # Если язык не установлен, показываем клавиатуру для выбора языка
        show_keyboard(user_id,"something wrong,try later")

#Метод реализующий вывод кастомной клавиатуры с опциями
def show_keyboard(user_id, call):
    if user_id in user_state and user_state[user_id]['language']:
        user_lang = user_state[user_id]['language']
        account_btn = get_translation(user_lang, "account_btn")
        settings_btn = get_translation(user_lang, "settings_btn")
        tariffs_btn = get_translation(user_lang, "tariffs_btn")
        allow_models_btn = get_translation(user_lang, "allow_models_btn")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(account_btn, settings_btn, allow_models_btn, tariffs_btn)

        bot.send_message(user_id, call, reply_markup=markup)

    else:
        get_user_lang(user_id)


# Сначала определим функцию, которая создает инлайн клавиатуру
def get_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    # Получаем переводы для кнопок
    settings_text = get_translation(user_lang, "settings_btn")
    buy_premium_text = get_translation(user_lang, "buy_premium_btn")

    # Создаем инлайн клавиатуру
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=settings_text, callback_data='settings'))
    markup.add(types.InlineKeyboardButton(text=buy_premium_text, callback_data='buy_premium'))

    return markup