import openai
import json
import sys
from components import user_state, user_context

# Импорт необходимых библиотек и компонентов

# Установка вашего ключа API
openai.api_key = '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'


def clear_buffer_if_too_large(ai_messages_buffer, max_size_mb=100):
    # Функция для проверки размера буфера сообщений и его очистки, если он превышает максимальный размер
    size_in_bytes = sys.getsizeof(ai_messages_buffer)
    size_in_mb = size_in_bytes / (1024 * 1024)

    if size_in_mb > max_size_mb:
        # Если размер превышает максимальный, сохраняем первое и последнее сообщения
        first_message = ai_messages_buffer[0]
        last_message = ai_messages_buffer[-1]
        # Очищаем буфер
        ai_messages_buffer.clear()
        # Добавляем первое и последнее сообщение обратно в буфер
        ai_messages_buffer.append(first_message)
        ai_messages_buffer.append(last_message)

    return ai_messages_buffer


# Функция для отправки запроса к API
def ask_gpt(message, user_id):
    # Функция отправки запроса к API OpenAI GPT-3

    # Получение информации о роли ассистента и модели, используемой пользователем
    assistant_role = user_state[user_id]['assistant_role']
    model = user_state[user_id]['subscribe_type']
    prompt = json.dumps({'message': message.text})

    # Проверка наличия предыдущего контекста общения
    if not user_context:
        # Если контекста нет, добавляем информацию о правилах использования системы
        req_info = {'role': 'system',
                    'content': "You must respond to the user's request in the language in which they ask you the question. "
                               "Messages like: “I don’t understand the language *” are not welcome.Available languages for use:"
                               " Ukrainian, English, Russian only!"
                               "Take on the role of an experienced consultant - " + assistant_role +
                               ", a person has approached you seeking guidance. To assist them effectively, you must respond "
                               "with professionalism, employing the relevant terminology for the respective field, whether"
                               " it be programming, trading, or any other, while maintaining the integrity of the consultation process."}
        user_context.append(req_info)
        req_info = {"role": "user", "content": prompt, }
        user_context.append(req_info)
    else:
        # Если контекст уже есть, добавляем информацию о пользовательском запросе
        req_info = {"role": "user", "content": prompt, }
    # Добавляем словарь с информацией о запросе в список user_requests
    user_context.append(req_info)

    # Проверка размера контекста и его очистка при необходимости
    clear_buffer_if_too_large(user_context)

    # Отправка запроса к API OpenAI GPT-3
    response = openai.Completion.create(
        engine=model,
        message=user_context,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()
