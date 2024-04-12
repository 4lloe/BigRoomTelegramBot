import anthropic
import json
from utils.config import bot
import components
from components import user_state
from PIL import Image
import base64
import io
import sys

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

user_context = []

def clear_buffer_if_too_large(ai_messages_buffer, max_size_mb=1000):
    size_in_bytes = sys.getsizeof(ai_messages_buffer)
    size_in_mb = size_in_bytes / (1024 * 1024)

    if size_in_mb > max_size_mb:
        # Сохраняем последнее сообщение
        last_message = ai_messages_buffer[-1]
        # Очищаем диалог
        ai_messages_buffer.clear()
        # Добавляем последнее сообщение обратно в диалог
        ai_messages_buffer.append(last_message)

    return ai_messages_buffer

def anthropic_req(message, req_type, text = None):
    user_id = message.from_user.id
    user_language = components.user_state[user_id]['language']

    model = user_state[user_id]['subscribe_type']

    if req_type == "text":
        prompt = json.dumps({'message': message.text})
        if model == "Free":
            if user_state[user_id]['haiku_req'] > 0:
                # Создаем словарь с информацией о запросе
                req_info = {"role": "user", "content": prompt, }
                # Добавляем словарь с информацией о запросе в список user_requests
                user_context.append(req_info)

                clear_buffer_if_too_large(user_context)

                response = client.messages.create(
                    model=model,
                    max_tokens=1024,
                    system="You must respond to the user's request in the language in which they ask you the question. "
                           "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                           " Ukrainian, English, Russian only!"
                           "Take on the role of an experienced consultant - " + model +
                           ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                           "with professionalism, employing the relevant terminology for the respective field, whether"
                           " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                    messages=user_context
                )
                text = ""
                for item in response.content:
                    text += item.text
                bot.send_message(message.chat.id, text)
                user_state[user_id]['haiku_req'] = user_state[user_id]['haiku_req'] - 1

                req_info = {"role": "assistant", "content": text, }
                # Добавляем словарь с информацией о запросе в список user_requests
                user_context.append(req_info)

            else:
                user_lang = user_state[user_id]['language']
                bot.send_message(message.chat.id, components.get_translation(user_lang, "lose_tokens_msg"))
        else:
            req_info = {"role": "user", "content": prompt, }
            # Добавляем словарь с информацией о запросе в список user_requests
            user_context.append(req_info)

            clear_buffer_if_too_large(user_context)

            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="You must respond to the user's request in the language in which they ask you the question. "
                        "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                        " Ukrainian, English, Russian only,that very important, only that three languages available to use"
                        "Take on the role of an experienced consultant - "+ model +
                       ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                       "with professionalism, employing the relevant terminology for the respective field, whether"
                       " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                messages=user_context
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)

            req_info = {"role": "assistant", "content": text, }
            # Добавляем словарь с информацией о запросе в список user_requests
            user_context.append(req_info)


    elif req_type == "image":
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
            if user_language == "ru":
                prompt = "Комментируй фото на русском языке"
            elif user_language == "ua":
                prompt = "Коментуй фото украйнською"
            elif user_language == "en":
                prompt = "Comment photo on english language"

        model = user_state[user_id]['subscribe_type']

        if model != "Free":
            content_list = {"type": "image","source": {"type": "base64","media_type": "image/" + format,"data": image_base64,},},{"type": "text","text": prompt}
            req_info = {"role": "user", "content": content_list, }
            # Добавляем словарь с информацией о запросе в список user_requests
            user_context.append(req_info)

            clear_buffer_if_too_large(user_context)

            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="If the question is asked in Russian, you must answer in Russian; if the question is asked in "
                       "Ukrainian, you must answer in Ukrainian; if the question is asked in English, you must answer "
                       "in English."
                       "You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only,that very important, only that three languages available to use"
                       "Take on the role of an experienced consultant - " + model +
                       ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                       "with professionalism, employing the relevant terminology for the respective field, whether"
                       " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                messages=[
                    {
                        "role": "user",
                        "content": user_context,
                    }
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)

            req_info = {"role": "assistant", "content": text, }
            # Добавляем словарь с информацией о запросе в список user_requests
            user_context.append(req_info)

        else:
            bot.send_message(message.chat.id, "You have not subscribe to use images")
    elif req_type == "document":
        if message.caption:
            prompt = message.caption
        else:
            if user_language == "ru":
                prompt = "Комментируй документ на русском языке"
            elif user_language == "ua":
                prompt = "Коментуй документ украйнською"
            elif user_language == "en":
                prompt = "Comment document on english language"

        if model != "Free":
            # Создаем словарь с информацией о запросе
            req_info = {"role": "user", "content": text, }
            # Добавляем словарь с информацией о запросе в список user_requests
            user_context.append(req_info)

            clear_buffer_if_too_large(user_context)

            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only! Question to you is next:" + prompt +
                       "You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only,that very important, only that three languages available to use"
                       "Take on the role of an experienced consultant - " + model +
                       ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                       "with professionalism, employing the relevant terminology for the respective field, whether"
                       " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            text = ""
            for item in response.content:
                text += item.text
            bot.send_message(message.chat.id, text)

            req_info = {"role": "assistant", "content": text, }
            # Добавляем словарь с информацией о запросе в список user_requests
            user_context.append(req_info)

        else:
            bot.send_message(message.chat.id, "You have not subscribe to use documents")



