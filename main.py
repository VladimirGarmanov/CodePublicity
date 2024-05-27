import time
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
import openai

client = openai.OpenAI(api_key="sk-proj-EHGl77fR7EDj8kmzxNaqT3BlbkFJLlgCMmYPHzTih7CKCU1V")
users = []

file1 = client.files.create(
  file=open("ТРЕБОВАНИЯ К СПИКЕРАМ.pdf", "rb"),
  purpose='assistants'
)
file2 = client.files.create(
  file=open("Основные_правила.txt", "rb"),
  purpose='assistants'
)
file3 = client.files.create(
  file=open("Ценности_сообщества_Код_публичности.docx", "rb"),
  purpose='assistants'
)


Assistant_ID = 'asst_k6CzohXqymAeteT2CDcvU0TY'
print(Assistant_ID)
TELEGRAM_TOKEN = '6832211064:AAGj7DTV_LqZSli9Xz2Yn-0g4oegrg_4aFM'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
threads = {}



# Функция для добавления пользователя в базу данных
async def handle_with_assistant(message, chat_id):
    print('генерация началась')
    thread_id = threads[chat_id]
    message_answer = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"{message.text} Если не знаешь этого, то посмотри в прикрепленных файлах Все файлы которые тебе нужны уже загружены"

    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=Assistant_ID,

    )

    time.sleep(10)
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )

    print(run_status.status)
    while run_status.status == 'in_progress':
        time.sleep(5)
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    print(run_status.status)
    if run_status.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        msg = messages.data[0]
        role = msg.role
        content = msg.content[0].text.value
        print(f"{role.capitalize()}: {content}")
        await bot.send_message(chat_id=message.chat.id, text=content)


def add_user(chat_id):

    thread = client.beta.threads.create()
    threads[chat_id] = thread.id
    print(thread.id)
    return thread.id


async def answer_user(message_response, message):
    await message.answer(message_response)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    add_user(message.chat.id)
    await message.answer("Привет! Вы зарегистрированы.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo_message(message: types.Message):
    await handle_with_assistant(message, message.chat.id)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)