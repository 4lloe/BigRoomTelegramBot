import json

telegrambot_token = "6981720034:AAFpPGkTreAt_WzUw65mPIxgMzdk4KJ2gV4"
language = "english"
LOCALES_DIR = 'locales/'

#!!!Заменить на БД
# Создаем словарь для хранения языка каждого пользователя (в реальном проекте это стоит сохранять в базе данных)
user_state = {}






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
    if user_id in user_language:
        return user_language[user_id]
    else:
        return 'en'
