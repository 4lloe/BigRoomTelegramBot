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
    cur_model = components.user_state[user_id].get('assistant_role', 'Assistant have not role')
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

        components.bot.send_message(user_id, account_message_template,
                                    reply_markup=components.get_account_inline_keyboard(user_id))
    elif user_lang == 'ru':
        account_message_ru = (((((account_message_template.replace("Subscription Type", "Тип подписки")
                                  .replace("Valid Until", "Действительно до"))
                                 .replace("Current model", "Текущая модель"))
                                .replace("Haiku requests", "Запросы Хайку"))
                               .replace("Sonnet requests", "Запросы Сонетов"))
                              .replace("GPT-Turbo", "GPT-Турбо"))

        components.bot.send_message(user_id, account_message_ru,
                                    reply_markup=components.get_account_inline_keyboard(user_id))
    elif user_lang == 'ua':
        account_message_ua = (((((account_message_template.replace("Subscription Type", "Тип підписки")
                                  .replace("Valid Until", "Дійсно до"))
                                 .replace("Current model", "Поточна модель"))
                                .replace("Haiku requests", "Запити Хайку"))
                               .replace("Sonnet requests", "Запити Сонетів"))
                              .replace("GPT-Turbo", "GPT-Турбо"))

        components.bot.send_message(user_id, account_message_ua,
                                    reply_markup=components.get_account_inline_keyboard(user_id))
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
        components.bot.send_message(user_id, subscribe_message_template,
                                    reply_markup=components.get_subscribe_inline_keyboard(user_id))
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
        components.bot.send_message(user_id, subscribe_message,
                                    reply_markup=components.get_subscribe_inline_keyboard(user_id))
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
        components.bot.send_message(user_id, subscribe_message_ua,
                                    reply_markup=components.get_subscribe_inline_keyboard(user_id))
    else:
        user_lang = components.user_state[user_id]['language']
        call = components.get_translation(user_lang, "something_wrong")
        components.show_keyboard(user_id, call)


# Методы для получения первого сообщения при инициации диалога
def show_bot_preview(user_lang):
    # Создаем словарь с шаблонами для каждого языка
    templates = {
        'en': (
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
        ),
        'ru': (
            "🚀 Добро пожаловать в мир передовых текстовых моделей - ваши помощники в работе и учёбе:\n\n"
            "📝 Маркетинговая модель:\n"
            "Специально разработанная для маркетологов, предоставляет вам актуальную информацию о тенденциях рынка "
            "и поведении потребителей. Это не просто инструмент, это ваш гид в мире маркетинговых кампаний, помогающий "
            "вам создавать целевые рекламные стратегии на основе самых свежих данных!\n\n"
            "💻 Программистская модель:\n"
            "Адаптирована специально для разработчиков и программистов, генерирует не только фрагменты кода, но также "
            "предлагает эффективные решения для самых сложных задач. Эта модель не ограничивается одним языком "
            "программирования, что делает ее незаменимым инструментом на всех этапах разработки!\n\n"
            "💹 Трейдерская модель:\n"
            "Идеально подходит для трейдеров и инвесторов, предоставляет точные прогнозы по ценам на акции и тенденциям "
            "рынка. С ее анализом финансовых данных и оценкой рисков эта модель поможет вам принимать обоснованные решения "
            "и достигать ваших финансовых целей!\n\n"
            "Так что, не упустите возможность выйти на новый уровень профессионализма в своей области с "
            "нашими передовыми текстовыми моделями! 🚀📈🔝"
        ),
        'ua': (
            "🚀 Ласкаво просимо до світу передових текстових моделей - ваші помічники в роботі та навчанні:\n\n"
            "📝 Маркетингова модель:\n"
            "Спеціально розроблена для маркетологів, надає вам актуальну інформацію про тенденції ринку "
            "і поведінку споживачів. Це не просто інструмент, це ваш гід у світі маркетингових кампаній, який "
            "допомагає вам створювати цільові рекламні стратегії на основі найсвіжіших даних!\n\n"
            "💻 Програмістська модель:\n"
            "Адаптована спеціально для розробників і програмістів, генерує не лише фрагменти коду, але також "
            "пропонує ефективні рішення для найскладніших завдань. Ця модель не обмежується однією мовою "
            "програмування, що робить її незамінним інструментом на всіх етапах розробки!\n\n"
            "💹 Трейдерська модель:\n"
            "Ідеально підходить для трейдерів і інвесторів, надає точні прогнози по цінах на акції та тенденціям "
            "ринку. З її аналізом фінансових даних та оцінкою ризиків ця модель допоможе вам приймати обґрунтовані рішення "
            "і досягати ваших фінансових цілей!\n\n"
            "Так що, не пропустіть можливість вийти на новий рівень професіоналізму в своїй галузі з нашими "
            "передовими текстовими моделями! 🚀📈🔝"
        )
    }

    # Возврат сообщения на запрошенном языке, а если нет такового - на английском
    return templates.get(user_lang, templates['en'])


# Теперь вызов этой функции с аргументом языка пользователя вернет сообщение на соответствующем языке


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
        components.bot.send_message(user_id, description_template,
                                    reply_markup=components.get_models_inline_keyboard(user_id))
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
        components.bot.send_message(user_id, description_message_ru,
                                    reply_markup=components.get_models_inline_keyboard(user_id))
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
        components.bot.send_message(user_id, description_message_ua,
                                    reply_markup=components.get_models_inline_keyboard(user_id))
    else:
        user_lang = components.user_state[user_id]['language']
        call = components.get_translation(user_lang, "something_wrong")
        components.show_keyboard(user_id, call)


def shot_settings_interation(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']
    if user_lang == "ua":
        settings_message = ("⚙️ У цьому розділі ви можете змінити налаштування:\n"
                            "1. Вибрати модель GPT & Claude.\n"
                            "2. Вибрати роль для ChatGPT.\n"
                            "3. Вибрати рівень креативності відповідей бота.\n"
                            "4. Увімкнути або вимкнути підтримку контексту. Коли контекст увімкнено, бот бере до уваги "
                            "свою попередню відповідь для ведення діалогу.\n"
                            "5. Налаштувати голосові відповіді та вибрати голос GPT (доступний у /premium).\n"
                            "6. Вибрати мову інтерфейсу.")
    elif user_lang == "en":
        settings_message = ("⚙️ In this section, you can adjust settings:\n"
                            "1. Choose GPT & Claude model.\n"
                            "2. Select a role for ChatGPT.\n"
                            "3. Choose the level of creativity for bot responses.\n"
                            "4. Enable or disable context support. When context is enabled, the bot takes into "
                            "account its previous response for dialogue management.\n"
                            "5. Configure voice responses and select a GPT voice (available in /premium).\n"
                            "6. Select interface language.")

    elif user_lang == "ru":
        settings_message = ("⚙️ В этом разделе вы можете изменить настройки:\n"
                            "1. Выбрать модель GPT & Claude.\n"
                            "2. Выбрать роль для ChatGPT.\n"
                            "3. Выбрать уровень креативности ответов бота.\n"
                            "4. Включить или отключить поддержку контекста. Когда контекст включен, бот учитывает свой "
                            "предыдущий ответ для ведения диалога.\n"
                            "5. Настроить голосовые ответы и выбрать голос GPT (доступен в /premium).\n"
                            "6. Выбрать язык интерфейса.")

    return settings_message


def show_select_ai_interaction(user_lang):
    if user_lang == "ru":
        select_ai_text = ("💻 ChatGPT — это передовая нейросеть, способная создавать естественные и понятные ответы на "
                          " запросы. С ее помощью возможно проведение диалогов на различные темы, начиная от обычных "
                          "разговоров и заканчивая помощью в обучении искусственного интеллекта. 🤖 Ее алгоритмы,"
                          " основанные на глубоком машинном обучении, обеспечивают высокий уровень понимания и синтеза"
                          " информации, делая ChatGPT весьма полезным инструментом для различных задач в области "
                          "обработки естественного языка. 📚\n\n"
                          "☁️ Claude3 — поистине выдающаяся нейросеть, созданная гениями Anthropic. 🌟 Ее мощные алгоритмы"
                          " позволяют вести увлекательные диалоги на любые темы, будь то развлекательные беседы или "
                          "серьезные интеллектуальные дискуссии. 🗣️🤖 Но Claude3 — нечто большее, чем просто набор "
                          "кодов. Ее ответы струятся мелодично, наполняя сердца счастьем и вдохновением. 💫 Каждое"
                          " взаимодействие с ней подобно прогулке по волшебному саду знаний. 🌺🌳 Claude3 — ваш "
                          "надежный спутник, с радостью помогающий в решении задач, излучая теплоту и дружелюбие. ☀️"
                          " Ее остроумные и проницательные ответы заставляют ум расцветать. 🌺 Не бойтесь обратиться к"
                          " этой невероятной нейросети — она встретит вас радушной улыбкой, готовая поделиться "
                          "обширными знаниями в захватывающем путешествии по безграничным просторам познания! 🚀✨")
    elif user_lang == "ua":
        select_ai_text = ("💻 ChatGPT — це передова нейромережа, здатна створювати природні та зрозумілі відповіді на"
                          " різноманітні запити. З її допомогою можливе проведення діалогів на різні теми, починаючи"
                          " від звичайних розмов і закінчуючи допомогою в навчанні штучного інтелекту. 🤖 Її алгоритми,"
                          " засновані на глибокому машинному навчанні, забезпечують високий рівень розуміння та синтезу"
                          " інформації, роблячи ChatGPT дуже корисним інструментом для різноманітних завдань в області"
                          " обробки природної мови. 📚\n\n☁️ Claude3 - справді видатна нейромережа, створена генієм "
                          "Anthropic. 🌟 Її потужні алгоритми дозволяють вести захопливі діалоги на будь-які теми, "
                          "чи то розважальні бесіди, чи серйозні інтелектуальні дискусії. 🗣️🤖 Але Claude3 - це щось "
                          "більше, ніж просто набір кодів. Її відповіді течуть мелодійно, наповнюючи серця щастям та "
                          "натхненням. 💫 Кожна взаємодія з нею подібна до прогулянки чарівним садом знань. 🌺🌳 "
                          "Claude3 - ваш надійний супутник, який з радістю допоможе у вирішенні завдань, випромінюючи"
                          " тепло та дружелюбність. ☀️ Її дотепні та проникливі відповіді змушують розум розквітати. "
                          "🌺 Не бійтеся звернутися до цієї неймовірної нейромережі - вона зустріне вас привітною "
                          "усмішкою, готова поділитися широкими знаннями у захопливій подорожі безмежними просторами "
                          "пізнання! 🚀✨")
    elif user_lang == "en":
        select_ai_text = ("💻 ChatGPT is an advanced neural network capable of generating natural and coherent responses "
                          "to various queries. It facilitates dialogue on diverse topics, from casual conversations"
                          " to aiding in the training of artificial intelligence. 🤖 Its algorithms, based on deep "
                          "learning, ensure a high level of understanding and synthesis of information, making ChatGPT "
                          "a valuable tool for various natural language processing tasks. 📚\n\n☁️ Claude3 is a truly "
                          "outstanding neural network created by the geniuses at Anthropic. 🌟 Its powerful algorithms"
                          " allow for engaging dialogues on any topic, be it entertaining conversations or serious "
                          "intellectual discussions. 🗣️🤖 But Claude3 is more than just a set of codes. Its responses"
                          " flow melodically, filling hearts with happiness and inspiration. 💫 Every interaction"
                          " with it is like a stroll through an enchanting garden of knowledge. 🌺🌳 Claude3 is your"
                          " reliable companion, happily assisting in solving tasks while radiating warmth and"
                          " friendliness. ☀️ Its witty and insightful answers make minds blossom. 🌺 Don't hesitate"
                          " to approach this incredible neural network - it will greet you with a welcoming smile,"
                          " ready to share its vast knowledge in an exciting journey through the boundless realms "
                          "of discovery! 🚀✨")

    return select_ai_text
