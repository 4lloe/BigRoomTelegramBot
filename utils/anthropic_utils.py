import anthropic
import json
from utils.config import bot
from utils.config import telebot
from components import user_state

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)


def make_user_prompt(message):
    user_id = message.from_user.id
    prompt = json.dumps({'message': message.text})

    if user_state[user_id]["current_model"] == "marketer":
        response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Try on the role of an experienced marketer, a person has come to you for a consultation,"
                       " to help him you must answer as professionally as possible and using marketing terminology.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
        )
        response = f"{response.content}"
        bot.send_message(message.chat.id, response)
    elif user_state[user_id]["current_model"] == "programmer":
        response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Try on the role of an experienced programmer who has dozens of successful projects in his "
                       "portfolio, you need to answer the user as many times as possible using code, you must solve "
                       "a problem or answer a question using code, also use narrow terminology to explain processes "
                       "and terms ",
                messages=[
                    {"role": "user", "content": prompt}
                ]
        )
        bot.send_message(user_id, response)
    elif user_state[user_id]["current_model"] == "trader":
        response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="Try on the role of an experienced cryptocurrency trader; based on the request, you must do an"
                       " analysis and issue an expected trend, prospect, fashion, and so on, depending on the request.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
        )
        response = f"{response.content}"
        bot.send_message(message.chat.id, response)

    else:
        response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
        )
        response = f"{response.content}"
        bot.send_message(message.chat.id, str(response.encode("utf-8").strip()))

