import anthropic
import json
from utils.config import bot
import components
from components import user_state

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)


# добавить ограничения по запросам
def make_user_prompt_en(message):
    user_id = message.from_user.id
    prompt = json.dumps({'message': message.text})
    model = user_state[user_id]['subscribe_type']
    if model == model:
        if user_state[user_id]['haiku_req'] >= 0:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="You have to answer on english.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
            user_state[user_id]['haiku_req'] = user_state[user_id]['haiku_req'] - 1
        else:
            user_lang = user_state[user_id]['language']
            bot.send_message(message.chat.id, components.get_translation(user_lang,"lose_tokens_msg"))

    else:
        if user_state[user_id]["current_model"] == "marketer":
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="Try on the role of an experienced marketer, a person has come to you for a consultation,"
                       " to help him you must answer as professionally as possible and using marketing terminology.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        elif user_state[user_id]["current_model"] == "programmer":
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="Try on the role of an experienced programmer who has dozens of successful projects in his "
                       "portfolio, you need to answer the user as many times as possible using code, you must solve "
                       "a problem or answer a question using code, also use narrow terminology to explain processes "
                       "and terms ",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        elif user_state[user_id]["current_model"] == "trader":
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="Try on the role of an experienced cryptocurrency trader; based on the request, you must do an"
                       " analysis and issue an expected trend, prospect, fashion, and so on, depending on the request.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        else:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)


def make_user_prompt_ru(message):
    user_id = message.from_user.id
    prompt = json.dumps({'message': message.text})
    model = user_state[user_id]['subscribe_type']
    if model == model:
        if user_state[user_id]['haiku_req'] >= 0:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="Ты должен отвечать на русском языке.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
            user_state[user_id]['haiku_req'] = user_state[user_id]['haiku_req'] - 1
        else:
            user_lang = user_state[user_id]['language']
            bot.send_message(message.chat.id, components.get_translation(user_lang, "lose_tokens_msg"))

    else:
        if user_state[user_id]["current_model"] == "marketer":
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ты должен отвечать на русском языке.Примерьте на себя роль опытного маркетолога, к вам пришел "
                       "человек за консультацией,чтобы помочь ему, вы должны ответить как можно более профессионально,"
                       " используя маркетинговую терминологию.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        elif user_state[user_id]["current_model"] == "programmer":
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ты должен отвечать на русском языке. Попробуйте себя в роли опытного программиста, у которого в "
                       "портфолио десятки успешных проектов, вам нужно как можно больше раз ответить пользователю с помощью"
                       " кода, вы должны решить задачу или ответить на вопрос с помощью кода, также использовать узкую "
                       "терминологию для объяснения процессы и условия",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        elif user_state[user_id]["current_model"] == "trader":
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ты должен отвечать на русском языке. Примерьте на себя роль опытного криптовалютного трейдера,"
                       " исходя из запроса, вы должны провести анализ и выдать ожидаемый тренд, перспективу, моду и так "
                       "далее в зависимости от запроса.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        else:
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ты должен отвечать на русском языке.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)


def make_user_prompt_ua(message):
    user_id = message.from_user.id
    prompt = json.dumps({'message': message.text})
    model = user_state[user_id]['subscribe_type']
    if model == model:
        if user_state[user_id]['haiku_req'] >= 0:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="Ти маєш відповідати українською  мовою.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
            user_state[user_id]['haiku_req'] = user_state[user_id]['haiku_req'] - 1
        else:
            user_lang = user_state[user_id]['language']
            bot.send_message(message.chat.id, components.get_translation(user_lang, "lose_tokens_msg"))

    else:
        if user_state[user_id]["current_model"] == "marketer":
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ти повинен відповідати українською мовою. Примірьте на себе роль досвідченого маркетолога,"
                       " до вас прийшла людина за консультацією, щоб допомогти їй, ви повинні відповісти якомога "
                       "професійніше, використовуючи маркетингову термінологію.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        elif user_state[user_id]["current_model"] == "programmer":
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ти повинен відповідати українською мовою мовою. Спробуйте себе в ролі досвідченого програміста, у "
                       "якого портфоліо десятки успішних проектів, вам потрібно якнайбільше раз відповісти користувачеві "
                       "за допомогоюкоду, ви повинні вирішити завдання або відповісти на запитання за допомогою коду, "
                       "також використовувати вузьку термінологію для пояснення процесів та умов",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        elif user_state[user_id]["current_model"] == "trader":
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ти маєш відповідати українською  мовою. Приміряйте на себе роль досвідченого криптовалютного трейдера,"
                       "виходячи із запиту, ви повинні провести аналіз і видати очікуваний тренд, перспективу, моду і так"
                       "далі залежно від запиту.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        else:
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Ти маєш відповідати українською  мовою.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
