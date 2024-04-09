import anthropic
import json
from utils.config import bot
import components
from components import user_state
from PIL import Image
import base64
import io

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)


# добавить ограничения по запросам
def make_user_prompt(message):
    user_id = message.from_user.id
    prompt = json.dumps({'message': message.text})
    model = user_state[user_id]['subscribe_type']
    if model == "Free":
        if user_state[user_id]['haiku_req'] > 0:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only!",
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
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only!"
                       "Try on the role of an experienced marketer, a person has come to you for a consultation,"
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
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only!"
                       "Try on the role of an experienced programmer who has dozens of successful projects in his "
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
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only!"
                       "Try on the role of an experienced cryptocurrency trader; based on the request, you must do an"
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


def user_document_prompt(text, message):
    user_id = message.from_user.id
    model = user_state[user_id]['subscribe_type']
    prompt = json.dumps({'message': message.text})

    if model != "Free":
        response = client.messages.create(
            model='claude-2.1',
            max_tokens=1024,
            system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only! Question to you is next:" + prompt,
            messages=[
                {"role": "user", "content": text}
            ]
        )
        text = ""
        for item in response.content:
            text += item.text
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "You have not subscribe to use documents")