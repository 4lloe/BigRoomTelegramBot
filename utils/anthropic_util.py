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
                messages=[{"role": "user", "content": prompt}]
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
                model=model,
                max_tokens=1024,
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only!"
                       "Try on the role of an experienced marketer, a person has come to you for a consultation,"
                       " to help him you must answer as professionally as possible and using marketing terminology.",
                messages=[{"role": "user", "content": prompt}]
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
                messages=[{"role": "user", "content": prompt}]
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
                       "Put on the role of an experienced trader who has a wealth of experience and successful transactions."
                       " You should answer the user's question as professionally as possible using trading terminology, "
                       "and be able to give advice on trading and investments.",
                messages=[{"role": "user", "content": prompt}]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)
        else:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)


def user_image_prompt(message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    format = image.format.lower()

    image_base64 = base64.b64encode(downloaded_file).decode('utf-8')

    user_id = message.from_user.id
    if message.caption:
        prompt = message.caption
    else:
        if user_lang == "ru":
            prompt = "Комментируй фото на русском языке"
        elif user_lang == "ua":
            prompt = "Коментуй фото украйнською"
        elif user_lang == "en":
            prompt = "Comment photo on english language"

    model = user_state[user_id]['subscribe_type']

    if model != "Free":
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system="If the question is asked in Russian, you must answer in Russian; if the question is asked in "
                   "Ukrainian, you must answer in Ukrainian; if the question is asked in English, you must answer "
                   "in English.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/" + format,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ]
        )
        text = ""
        for item in response.content:
            text += item.text
        bot.send_message(message.chat.id, text)

    else:
        bot.send_message(message.chat.id, "You have not subscribe to use images")


def user_document_prompt(text, message):
    user_id = message.from_user.id
    user_lang = components.user_state[user_id]['language']

    user_id = message.from_user.id
    model = user_state[user_id]['subscribe_type']

    if message.caption:
        prompt = message.caption
    else:
        if user_lang == "ru":
            prompt = "Комментируй документ на русском языке"
        elif user_lang == "ua":
            prompt = "Коментуй документ украйнською"
        elif user_lang == "en":
            prompt = "Comment document on english language"

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
