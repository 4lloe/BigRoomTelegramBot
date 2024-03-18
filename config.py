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

        bot.send_message(user_id, account_message_template, reply_markup=get_account_inline_keyboard(user_id))
    elif user_lang == 'ru':
        account_message_ru = (((((account_message_template.replace("Subscription Type", "Тип подписки")
                              .replace("Valid Until", "Действительно до"))
                              .replace("Current model", "Текущая модель"))
                              .replace("Haiku requests", "Запросы Хайку"))
                              .replace("Sonnet requests", "Запросы Сонетов"))
                              .replace("GPT-Turbo", "GPT-Турбо"))

        bot.send_message(user_id,  account_message_ru, reply_markup=get_account_inline_keyboard(user_id))
    elif user_lang == 'ua':
        account_message_ua = (((((account_message_template.replace("Subscription Type", "Тип підписки")
                              .replace("Valid Until", "Дійсно до"))
                              .replace("Current model", "Поточна модель"))
                              .replace("Haiku requests", "Запити Хайку"))
                              .replace("Sonnet requests", "Запити Сонетів"))
                              .replace("GPT-Turbo", "GPT-Турбо"))

        bot.send_message(user_id, account_message_ua, reply_markup=get_account_inline_keyboard(user_id))
    else:
        # Если язык не установлен, показываем клавиатуру для выбора языка
        show_keyboard(user_id,"something wrong,try later")


def show_subscribe(message):
    user_id = message.from_user.id
    user_lang = user_state[user_id]['language']
    subscribe_message_template = (
        "Are you looking for enhanced capabilities and increased request limits for your bot? "
        "Consider our subscriptions, which offer additional features and extended limits, "
        "as well as the option to purchase requests separately:\n\n"
        "👌 Starter:\n"
        "— Subscription to Claude 3 Haiku — up to 100 requests per day.\n"
        "— Ideally suited for creating concise haiku poetry and text generation.\n"
        "— Ad-free experience.\n"
        "— Priority server access for accelerated response retrieval.\n"
        "— 10% discount on purchasing additional Claude tokens and requests.\n\n"
        "🌉 Intermediate:\n"
        "— Subscription to Claude 3 Sonnet — up to 150 requests per day.\n"
        "— Ability to create structured sonnets and poetry.\n"
        "— Continuous access with no delays between requests.\n"
        "— Advanced configuration options for precise bot functionality tuning.\n"
        "— Increased context size for improved response accuracy.\n"
        "— 15% discount on purchasing additional Claude tokens and requests.\n\n"
        "🚀 Advanced:\n"
        "— Subscription to ChatGPT Turbo with plugins — unlimited requests per day.\n"
        "— Group chat support in Telegram groups.\n"
        "— Plugin integration for extended functionality.\n"
        "— External API integration for accessing global network information and utilizing it in responses.\n"
        "— 20% discount on purchasing additional Claude tokens and requests.\n"
        "— Early access to beta versions of new products and neural networks.\n\n"
        "These subscriptions are designed for those who aim to maximize the potential of their bot "
        "and ensure efficient interaction with artificial intelligence on the Telegram platform."
    )

    if user_lang == 'en':
        bot.send_message(user_id, subscribe_message_template)
    elif user_lang == 'ru':
        subscribe_message = subscribe_message_template.replace(
            "Are you looking for enhanced capabilities and increased request limits for your bot?",
            "Вы ищете расширенные возможности и увеличенный лимит запросов для вашего бота?") \
            .replace("Consider our subscriptions,", "Рассмотрите наши подписки,") \
            .replace("as well as the option to purchase requests separately:",
                     "а также возможность отдельного приобретения запросов:") \
            .replace("Subscription to", "Подписка на") \
            .replace("requests per day", "запросов в день") \
            .replace("unlimited requests per day", "неограниченное количество запросов в день") \
            .replace("Ad-free experience.", "Отсутствие рекламных вставок.") \
            .replace("Priority server access for accelerated response retrieval.",
                     "Приоритетный доступ к серверам для ускоренного получения ответов.") \
            .replace("discount on purchasing additional", "скидка на покупку дополнительных") \
            .replace("Early access to beta versions of new products and neural networks.",
                     "Предварительный доступ к бета-версиям новых продуктов и нейронных сетей.") \
            .replace("These subscriptions are designed for those who aim to",
                     "Эти подписки предназначены для тех, кто стремится") \
            .replace("and ensure efficient interaction with artificial intelligence on the Telegram platform.",
                     "и обеспечить эффективное взаимодействие с искусственным интеллектом на платформе Telegram.")
        bot.send_message(user_id, subscribe_message)
    elif user_lang == 'ua':
        # Перевод текста подписки на украинский язык
        subscribe_message_ua = (((((((((((subscribe_message_template.replace(
            "Are you looking for enhanced capabilities and increased request limits for your bot?",
            "Ви шукаєте розширені можливості та збільшений ліміт запитів для вашого бота?")
                                .replace("Consider our subscriptions,", "Розгляньте наші підписки,"))
                                .replace("as well as the option to purchase requests separately:",
                 "а також можливість окремого придбання запитів:"))
                                .replace("Subscription to", "Підписка на"))
                                .replace("requests per day", "запитів на день"))
                                .replace("unlimited requests per day", "необмежена кількість запитів на день"))
                                .replace("Ad-free experience.", "Досвід без реклами."))
                                .replace("Priority server access for accelerated response retrieval.",
                 "Пріоритетний доступ до серверів для прискореного отримання відповідей."))
                                .replace("discount on purchasing additional", "знижка при купівлі додаткових"))
                                .replace("Early access to beta versions of new products and neural networks.",
                 "Достроковий доступ до бета-версій нових продуктів та нейронних мереж."))
                                .replace("These subscriptions are designed for those who aim to", "Ці підписки призначені для тих, хто прагне"))
                                .replace("and ensure efficient interaction with artificial intelligence on the Telegram platform.",
                 "та забезпечити ефективну взаємодію з штучним інтелектом на платформі Telegram."))
        bot.send_message(user_id, subscribe_message_ua)
    else:
        user_lang = user_state[user_id]['language']
        call = get_translation(user_lang, "something_wrong")
        show_keyboard(user_id, call)





#Метод реализующий вывод кастомной клавиатуры с опциями
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


# Сначала определим функцию, которая создает инлайн клавиатуру
def get_account_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    # Получаем переводы для кнопок
    settings_text = get_translation(user_lang, "settings_btn")
    buy_premium_text = get_translation(user_lang, "buy_subscribe_btn")

    # Создаем инлайн клавиатуру
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⚙️"+settings_text, callback_data='settings'))
    markup.add(types.InlineKeyboardButton(text="🌠"+buy_premium_text, callback_data='buy_subscribe'))

    return markup

def get_settings_inline_keyboard(user_id):
    user_lang = user_state[user_id]['language']

    voice_text = get_translation(user_lang, "sb_voice_answers_btn")
    creativity_text = get_translation(user_lang, "sb_answers_creativity_btn")
    language_change_text = get_translation(user_lang, "sb_language_change_btn")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🗣️"+voice_text, callback_data='voice_settings'))
    markup.add(types.InlineKeyboardButton(text="🎨"+creativity_text, callback_data='creativity_settings'))
    markup.add(types.InlineKeyboardButton(text="🇺🇦"+language_change_text, callback_data='language_settings'))
    markup.add(types.InlineKeyboardButton(text="Close",callback_data='close_btn'))

    return markup
