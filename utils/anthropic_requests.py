import anthropic
import json
from utils.config import bot  # Импортируем бота для отправки сообщений
import components  # Импортируем компоненты для работы с состоянием пользователя
from components import user_state, user_context  # Импортируем состояние пользователя и контекст пользователя
from PIL import Image  # Импортируем модуль для работы с изображениями
import base64  # Импортируем модуль для работы с base64
import io  # Импортируем модуль для работы с потоками данных
import sys  # Импортируем модуль для работы с системными параметрами

# Инициализируем клиента Anthropica с использованием API-ключа
client = anthropic.Anthropic(
    api_key="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"
)

# Функция для очистки буфера сообщений, если он слишком большой
def clear_buffer_if_too_large(ai_messages_buffer, max_size_mb=100):
    size_in_bytes = sys.getsizeof(ai_messages_buffer)
    size_in_mb = size_in_bytes / (1024 * 1024)

    if size_in_mb > max_size_mb:
        last_message = ai_messages_buffer[-1]  # Сохраняем последнее сообщение
        ai_messages_buffer.clear()  # Очищаем диалог
        ai_messages_buffer.append(last_message)  # Добавляем последнее сообщение обратно в диалог

    return ai_messages_buffer

# Функция для отправки запроса к Anthropica
def anthropic_req(message, req_type, text=None):
    user_id = message.from_user.id
    user_language = components.user_state[user_id]['language']  # Получаем язык пользователя из состояния

    model = user_state[user_id]['subscribe_type']  # Получаем тип модели из состояния пользователя
    assistant_role = user_state[user_id]['assistant_role']  # Получаем роль ассистента из состояния пользователя

    # Обработка текстового запроса
    if req_type == "text":
        prompt = json.dumps({'message': message.text})  # Создаем JSON с текстом сообщения

        # Если подписка бесплатная и есть запросы на хайку
        if model == "Free" and user_state[user_id]['haiku_req'] > 0:
            req_info = {"role": "user", "content": prompt}  # Создаем информацию о запросе
            user_context.append(req_info)  # Добавляем запрос в контекст пользователя

            clear_buffer_if_too_large(user_context)  # Очищаем буфер, если необходимо

            # Создаем запрос к Anthropica
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only!"
                       "Take on the role of an experienced consultant - " + assistant_role +
                       ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                       "with professionalism, employing the relevant terminology for the respective field, whether"
                       " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                messages=user_context
            )

            # Получаем текст ответа от Anthropica
            text = ""
            for item in response.content:
                text += item.text

            bot.send_message(message.chat.id, text)  # Отправляем ответ пользователю

            # Уменьшаем счетчик запросов на хайку
            user_state[user_id]['haiku_req'] = user_state[user_id]['haiku_req'] - 1

            # Добавляем информацию о запросе в контекст пользователя
            req_info = {"role": "assistant", "content": text}
            user_context.append(req_info)

        else:
            user_lang = user_state[user_id]['language']  # Получаем язык пользователя
            bot.send_message(message.chat.id, components.get_translation(user_lang, "lose_tokens_msg"))

    # Обработка изображения
    elif req_type == "image":
        file_info = bot.get_file(message.photo[-1].file_id)  # Получаем информацию о файле изображения
        downloaded_file = bot.download_file(file_info.file_path)  # Загружаем файл изображения

        image_stream = io.BytesIO(downloaded_file)  # Создаем поток для изображения
        image = Image.open(image_stream)  # Открываем изображение
        format = image.format.lower()  # Получаем формат изображения

        image_base64 = base64.b64encode(downloaded_file).decode('utf-8')  # Кодируем изображение в base64

        # Получаем подписку пользователя и создаем соответствующий prompt
        model = user_state[user_id]['subscribe_type']
        if message.caption:
            prompt = message.caption
        else:
            if user_language == "ru":
                prompt = "Комментируй фото на русском языке"
            elif user_language == "ua":
                prompt = "Коментуй фото українською"
            elif user_language == "en":
                prompt = "Comment photo on english language"

        # Если подписка не бесплатная
        if model != "Free":
            content_list = [{"type": "image","source": {"type": "base64","media_type": "image/" + format,"data": image_base64},},{"type": "text","text": prompt}]
            req_info = {"role": "user", "content": content_list}  # Создаем информацию о запросе
            user_context.append(req_info)  # Добавляем запрос в контекст пользователя

            clear_buffer_if_too_large(user_context)  # Очищаем буфер, если необходимо

            # Создаем запрос к Anthropica
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system="If the question is asked in Russian, you must answer in Russian; if the question is asked in "
                       "Ukrainian, you must answer in Ukrainian; if the question is asked in English, you must answer "
                       "in English."
                       "You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       "Ukrainian, English, Russian only,that very important, only that three languages available to "
                       "use. Take on the role of an experienced consultant - " + assistant_role +
                       ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                       "with professionalism, employing the relevant terminology for the respective field, whether"
                       " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                messages=user_context
            )

            # Получаем текст ответа от Anthropica
            text = ""
            for item in response.content:
                text += item.text

            bot.send_message(message.chat.id, text)  # Отправляем ответ пользователю

            # Добавляем информацию о запросе в контекст пользователя
            req_info = {"role": "assistant", "content": text}
            user_context.append(req_info)

        else:
            bot.send_message(message.chat.id, "You have not subscribed to use images")

    # Обработка документа
    elif req_type == "document":
        if message.caption:
            prompt = message.caption
        else:
            if user_language == "ru":
                prompt = "Комментируй документ на русском языке"
            elif user_language == "ua":
                prompt = "Коментуй документ українською"
            elif user_language == "en":
                prompt = "Comment document on english language"

        # Если подписка не бесплатная
        if model != "Free":
            req_info = {"role": "user", "content": text}  # Создаем информацию о запросе
            user_context.append(req_info)  # Добавляем запрос в контекст пользователя

            clear_buffer_if_too_large(user_context)  # Очищаем буфер, если необходимо

            # Создаем запрос к Anthropica
            response = client.messages.create(
                model='claude-2.1',
                max_tokens=1024,
                system="You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only! Question to you is next:" + prompt +
                       "You must respond to the user's request in the language in which they ask you the question. "
                       "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                       " Ukrainian, English, Russian only,that very important, only that three languages available to use"
                       "Take on the role of an experienced consultant - " + assistant_role +
                       ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                       "with professionalism, employing the relevant terminology for the respective field, whether"
                       " it be programming, trading, or any other, while maintaining the integrity of the consultation process.",
                messages=[{"role": "user", "content": text}]
            )

            # Получаем текст ответа от Anthropica
            text = ""
            for item in response.content:
                text += item.text

            bot.send_message(message.chat.id, text)  # Отправляем ответ пользователю

            # Добавляем информацию о запросе в контекст пользователя
            req_info = {"role": "assistant", "content": text}
            user_context.append(req_info)

        else:
            bot.send_message(message.chat.id, "You have not subscribed to use documents")

