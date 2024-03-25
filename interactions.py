import components


# Методы для получения описания модели Маркетолога
def marketer_model_description(lang_code):
    descriptions = {
        'en': "📝 Marketer Model:\n"
              "Step 1: Conduct audience analysis 🎯\n"
              "Step 2: Ask about marketing trends and audience behavior 🎯\n"
              "Step 3: Get insights for creating effective advertising strategies with the latest data! 💡",

        'ru': "📝 Модель Маркетолога:\n"
              "Шаг 1: Проведите анализ целевой аудитории 🎯\n"
              "Шаг 2: Задайте вопрос о трендах в маркетинге и поведении аудитории 🎯\n"
              "Шаг 3: Получите инсайты для создания эффективных рекламных стратегий с учетом самых свежих данных! 💡",

        'ua': "📝 Модель Маркетолога:\n"
              "Крок 1: Проведіть аналіз цільової аудиторії 🎯\n"
              "Крок 2: Запитайте про тренди в маркетингу та поведінку аудиторії 🎯\n"
              "Крок 3: Отримайте інсайти для створення ефективних рекламних стратегій з урахуванням найсвіжіших даних! 💡"
    }
    return descriptions[lang_code]


# Методы для получения описания модели Программиста
def programmer_model_description(lang_code):
    descriptions = {
        'en': "💻 Programmer Model:\n"
              "Step 1: Define your development needs 💻\n"
              "Step 2: Formulate the task or problem you're facing 🔍\n"
              "Step 3: Receive a ready-made solution or code advice to move forward confidently! 🔧",

        'ru': "💻 Модель Программиста:\n"
              "Шаг 1: Определите свои потребности в разработке 💻\n"
              "Шаг 2: Сформулируйте задачу или проблему, с которой вы столкнулись 🔍\n"
              "Шаг 3: Получите готовое решение или советы по коду, чтобы продвигаться дальше с уверенностью! 🔧",

        'ua': "💻 Модель Програміста:\n"
              "Крок 1: Визначте свої потреби у розробці 💻\n"
              "Крок 2: Сформулюйте завдання чи проблему, з якою ви стикаєтесь 🔍\n"
              "Крок 3: Отримайте готове рішення чи поради по коду, щоб рухатися вперед впевнено! 🔧"
    }
    return descriptions[lang_code]


# Методы для получения описания модели Трейдера
def trader_model_description(lang_code):
    descriptions = {
        'en': "💹 Trader Model:\n"
              "Step 1: Define your investment goals 💰\n"
              "Step 2: Ask about price forecasts for stocks or cryptocurrencies 📊\n"
              "Step 3: Receive accurate data and advice to make the right financial decisions! 💹",

        'ru': "💹 Модель Трейдера:\n"
              "Шаг 1: Определите свои цели в инвестициях 💰\n"
              "Шаг 2: Задайте вопрос о прогнозах цен на акции или криптовалюты 📊\n"
              "Шаг 3: Получите точные данные и советы, чтобы сделать правильные финансовые решения! 💹",

        'ua': "💹 Модель Трейдера:\n"
              "Крок 1: Визначте свої цілі в інвестиціях 💰\n"
              "Крок 2: Запитайте про прогнози цін на акції чи криптовалюти 📊\n"
              "Крок 3: Отримайте точні дані та поради, щоб зробити правильні фінансові рішення! 💹"
    }
    return descriptions[lang_code]

# Методы для получения аккаунта пользователя
def show_account(user_id):
    user_lang = components.user_state[user_id]["language"]
    subscribe_type = components.user_state[user_id].get('subscribe_type', 'Free')
    valid_until = components.user_state[user_id].get('valid_until', '2024-03-19')
    cur_model = components.user_state[user_id].get('current_model', 'Free model')
    haiku_req = components.user_state[user_id].get('haiku_req', '2')
    sonnet_req = components.user_state[user_id].get('sonnet_req', '0')
    gpt_turbo_req = components.user_state[user_id].get('gpt_turbo_req', '0')

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

        components.bot.send_message(user_id, account_message_template, reply_markup=components.get_account_inline_keyboard(user_id))
    elif user_lang == 'ru':
        account_message_ru = (((((account_message_template.replace("Subscription Type", "Тип подписки")
                                  .replace("Valid Until", "Действительно до"))
                                 .replace("Current model", "Текущая модель"))
                                .replace("Haiku requests", "Запросы Хайку"))
                               .replace("Sonnet requests", "Запросы Сонетов"))
                              .replace("GPT-Turbo", "GPT-Турбо"))

        components.bot.send_message(user_id, account_message_ru, reply_markup=components.get_account_inline_keyboard(user_id))
    elif user_lang == 'ua':
        account_message_ua = (((((account_message_template.replace("Subscription Type", "Тип підписки")
                                  .replace("Valid Until", "Дійсно до"))
                                 .replace("Current model", "Поточна модель"))
                                .replace("Haiku requests", "Запити Хайку"))
                               .replace("Sonnet requests", "Запити Сонетів"))
                              .replace("GPT-Turbo", "GPT-Турбо"))

        components.bot.send_message(user_id, account_message_ua, reply_markup=components.get_account_inline_keyboard(user_id))
    else:
        # Если язык не установлен, показываем клавиатуру для выбора языка
        components.show_keyboard(user_id, "something wrong,try later")

# Методы для получения информации о доступных подписках
def subscribe_text(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']
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
        components.bot.send_message(user_id, subscribe_message_template, reply_markup=components.get_subscribe_inline_keyboard(user_id))
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
        components.bot.send_message(user_id, subscribe_message, reply_markup=components.get_subscribe_inline_keyboard(user_id))
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
                                 .replace("These subscriptions are designed for those who aim to",
                                          "Ці підписки призначені для тих, хто прагне"))
                                .replace("and ensure efficient interaction with artificial intelligence on the"
                                         " Telegram platform.", "та забезпечити ефективну взаємодію з штучним "
                                                                "інтелектом на платформі Telegram."))
        components.bot.send_message(user_id, subscribe_message_ua, reply_markup=components.get_subscribe_inline_keyboard(user_id))
    else:
        user_lang = components.user_state[user_id]['language']
        call = components.get_translation(user_lang, "something_wrong")
        components.show_keyboard(user_id, call)

# Методы для получения первого сообщения при инициации диалога
def show_bot_preview(user_lang):
    subscribe_message_template = (
        "🚀 Welcome to the world of advanced text models - your helpers in work and learning:\n\n"
        "📝 Marketing Model:\n"
        "Specially designed for marketing professionals, provides you with up-to-date information on market trends "
        "and consumer behavior. It's not just a tool, it's your guide in the world of marketing campaigns, helping "
        "you create targeted advertising strategies based on the freshest data!\n\n"
        "💻 Programmer Model:\n"
        "Adapted specifically for developers and programmers, generates not only code snippets but also offers "
        "effective solutions for the most complex tasks. This model is not limited to one programming language, "
        "making it an indispensable tool at all stages of development!\n\n"
        "💹 Trader Model:\n"
        "Perfect for traders and investors, provides accurate forecasts on stock prices and market trends. With its "
        "analysis of financial data and risk assessment, this model will help you make informed decisions and achieve "
        "your financial goals!\n\n"
        "So don't miss the opportunity to take your professionalism to the next level in your field with our "
        "advanced text models! 🚀📈🔝"
    )

    if user_lang == 'en':
        return subscribe_message_template
    elif user_lang == 'ru':
        subscribe_message = subscribe_message_template.replace(
            "🚀 Welcome to the world of advanced text models - your helpers in work and learning:",
            "🚀 Добро пожаловать в мир передовых текстовых моделей - ваши помощники в работе и учёбе:"
        ).replace("So don't miss the opportunity to take your professionalism to the next level in your field with our "
                  "advanced text models! 🚀📈🔝",
                  "Так что, не упустите возможность выйти на новый уровень профессионализма в своей области с "
                  "нашими передовыми текстовыми моделями! 🚀📈🔝"
                  )
        return subscribe_message
    elif user_lang == 'ua':
        subscribe_message_ua = subscribe_message_template.replace(
            "🚀 Welcome to the world of advanced text models - your helpers in work and learning:",
            "🚀 Ласкаво просимо до світу передових текстових моделей - ваші помічники в роботі та навчанні:"
        ).replace("So don't miss the opportunity to take your professionalism to the next level in your field with our "
                  "advanced text models! 🚀📈🔝",
                  "Так що, не пропустіть можливість вийти на новий рівень професіоналізму в своїй галузі з нашими "
                  "передовими текстовими моделями! 🚀📈🔝"
                  )
        return subscribe_message_ua
    else:
        return subscribe_message_template

# Методы для получения описания моделей
def model_description(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']
    description_template = (
        "📝 Marketer Model:\n"
        "— This model is specifically designed for marketing professionals.\n"
        "— It provides insights into market trends and consumer behavior.\n"
        "— Helps in creating targeted advertising campaigns.\n\n"
        "💻 Programmer Model:\n"
        "— Tailored for developers and programmers.\n"
        "— Generates code snippets and provides solutions to coding problems.\n"
        "— Supports multiple programming languages.\n\n"
        "💹 Trader Model:\n"
        "— Ideal for traders and investors in financial markets.\n"
        "— Offers predictions on stock prices and market trends.\n"
        "— Provides analysis of financial data and risk assessment.\n\n"
        "These models are designed to assist professionals in various fields "
        "by providing accurate and relevant text generation capabilities."
    )

    if user_lang == 'en':
        components.bot.send_message(user_id, description_template, reply_markup=components.get_models_inline_keyboard(user_id))
    elif user_lang == 'ru':
        description_message_ru = (description_template
                                  .replace("Marketer Model:", "Модель для Маркетологов:")
                                  .replace("— This model is specifically designed for marketing professionals.",
                                           "— Эта модель специально разработана для профессионалов маркетинга.")
                                  .replace("— It provides insights into market trends and consumer behavior.",
                                           "— Она предоставляет информацию о тенденциях на рынке и поведении потребителей.")
                                  .replace("— Helps in creating targeted advertising campaigns.",
                                           "— Помогает в создании целевых рекламных кампаний.")
                                  .replace("Programmer Model:", "Модель для Программистов:")
                                  .replace("— Tailored for developers and programmers.",
                                           "— Предназначена для разработчиков и программистов.")
                                  .replace("— Generates code snippets and provides solutions to coding problems.",
                                           "— Генерирует фрагменты кода и предоставляет решения для задач по программированию.")
                                  .replace("— Supports multiple programming languages.",
                                           "— Поддерживает несколько языков программирования.")
                                  .replace("Trader Model:", "Модель для Трейдеров:")
                                  .replace("— Ideal for traders and investors in financial markets.",
                                           "— Идеально подходит для трейдеров и инвесторов на финансовых рынках.")
                                  .replace("— Offers predictions on stock prices and market trends.",
                                           "— Предлагает прогнозы цен акций и рыночных тенденций.")
                                  .replace("— Provides analysis of financial data and risk assessment.",
                                           "— Проводит анализ финансовых данных и оценку рисков.")
                                  .replace("These models are designed to assist professionals in various fields",
                                           "Эти модели разработаны чтобы помочь профессионалам в различных областях")
                                  .replace("by providing accurate and relevant text generation capabilities.",
                                           "предоставляя точные и актуальные возможности для генерации текста."))
        components.bot.send_message(user_id, description_message_ru, reply_markup=components.get_models_inline_keyboard(user_id))
    elif user_lang == 'ua':
        description_message_ua = (description_template.replace("Marketer Model:", "Модель Маркетолога:")
                                  .replace("— This model is specifically designed for marketing professionals.",
                                           "— Ця модель створена спеціально для фахівців з маркетингу.")
                                  .replace("— It provides insights into market trends and consumer behavior.",
                                           "— Вона надає уявлення про тренди ринку та поведінку споживачів.")
                                  .replace("— Helps in creating targeted advertising campaigns.",
                                           "— Допомагає у створенні цільових рекламних кампаній.")
                                  .replace("Programmer Model:", "Модель Програміста:")
                                  .replace("— Tailored for developers and programmers.",
                                           "— Адаптована для розробників та програмістів.")
                                  .replace("— Generates code snippets and provides solutions to coding problems.",
                                           "— Генерує фрагменти коду та пропонує рішення для проблем програмування.")
                                  .replace("— Supports multiple programming languages.",
                                           "— Підтримує кілька мов програмування.")
                                  .replace("Trader Model:", "Модель Трейдера:")
                                  .replace("— Ideal for traders and investors in financial markets.",
                                           "— Ідеально підходить для трейдерів та інвесторів на фінансових ринках.")
                                  .replace("— Offers predictions on stock prices and market trends.",
                                           "— Пропонує прогнози щодо цін на акції та ринкових тенденцій.")
                                  .replace("— Provides analysis of financial data and risk assessment.",
                                           "— Надає аналіз фінансових даних та оцінку ризиків.")
                                  .replace("These models are designed to assist professionals in various fields",
                                           "Ці моделі призначені для допомоги професіоналам у різних галузях")
                                  .replace("by providing accurate and relevant text generation capabilities.",
                                           "шляхом надання точних та актуальних можливостей генерації тексту."))
        components.bot.send_message(user_id, description_message_ua, reply_markup=components.get_models_inline_keyboard(user_id))
    else:
        user_lang = components.user_state[user_id]['language']
        call = components.get_translation(user_lang, "something_wrong")
        components.show_keyboard(user_id, call)


