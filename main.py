import time
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
import openai

client = openai.OpenAI(api_key="сюда api key")
users = []

file1 = client.files.create(
  file=open("ТРЕБОВАНИЯ К СПИКЕРАМ.pdf", "rb"),
  purpose='assistants'
)

file2 = client.files.create(
  file=open("ПРАВИЛА_УЧАСТИЯ_В_МАСТЕРМАЙНДАХ_СООБЩЕСТВА_1.docx", "rb"),
  purpose='assistants'
)

file3 = client.files.create(
  file=open("Ценности_сообщества_Код_публичности.docx", "rb"),
  purpose='assistants'
)

file4 = client.files.create(
  file=open("Вопросы.docx", "rb"),
  purpose='assistants'
)

file5 = client.files.create(
  file=open("Вопросы-Ответы.docx", "rb"),
  purpose='assistants'
)


file7 = client.files.create(
  file=open("Город от 10 до 30 модераторов.pdf", "rb"),
  purpose='assistants'
)

file8 = client.files.create(
  file=open("Комитет_по_работе_с_модераторами.docx", "rb"),
  purpose='assistants'
)

file9 = client.files.create(
  file=open("Комитеты_и_Структура_взаимодействия.docx", "rb"),
  purpose='assistants'
)

file10 = client.files.create(
  file=open("Общая структура инструкции.docx", "rb"),
  purpose='assistants'
)

file11 = client.files.create(
  file=open("ПРАВИЛА_УЧАСТИЯ_В_МАСТЕРМАЙНДАХ_СООБЩЕСТВА_1.docx", "rb"),
  purpose='assistants'
)

file12 = client.files.create(
  file=open("ПРОЦЕССЫ комитета HR.docx", "rb"),
  purpose='assistants'
)

file13 = client.files.create(
  file=open("Рабочая_группа_КОМИТЕТ_PR_new __копия.docx", "rb"),
  purpose='assistants'
)

file14 = client.files.create(
  file=open("Распределение_функционала_куратора.docx", "rb"),
  purpose='assistants'
)

file15 = client.files.create(
  file=open("Рекомендованные_нижние_планки_на_стоимость_спонсорских_пакетов.docx", "rb"),
  purpose='assistants'
)

file16 = client.files.create(
  file=open("СИТУАЦИЯ был куратор и ушел.docx", "rb"),
  purpose='assistants'
)

file17 = client.files.create(
  file=open("Структура_работы_куратора_модератора_города_Лист1.pdf", "rb"),
  purpose='assistants'
)

file18 = client.files.create(
  file=open("ТРЕБОВАНИЯ К СПИКЕРАМ.pdf", "rb"),
  purpose='assistants'
)

file19 = client.files.create(
  file=open("Функции_и_полномочия_Кураторов_Ответы_Ответы_на_форму_1.pdf", "rb"),
  purpose='assistants'
)

file20 = client.files.create(
  file=open("Ценности_сообщества_Код_публичности.docx", "rb"),
  purpose='assistants'
)

file21 = client.files.create(
  file=open("Часто_задаваемые_вопросы_для_участников.docx", "rb"),
  purpose='assistants'
)

file22 = client.files.create(
  file=open("Часть 1 Набор группы.docx", "rb"),
  purpose='assistants'
)

file23 = client.files.create(
  file=open("Часть 2 Запуск группы.docx", "rb"),
  purpose='assistants'
)

file24 = client.files.create(
  file=open("Часть 3 Механика работы в группе.docx", "rb"),
  purpose='assistants'
)

file25 = client.files.create(
  file=open("Часть 4_Окончание_работы_и_выпускной.docx", "rb"),
  purpose='assistants'
)

assistant = client.beta.assistants.create(
  name="Код Публичности",
  description="Никогда не говори, что ты взял информацию из какого то файла, про бери информацию и пиши. Используй кодировку для телеграмм бота",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file1.id, file2.id, file3.id, file4.id, file5.id, file7.id, file8.id, file9.id, file10.id, file11.id, file12.id, file13.id, file14.id, file15.id, file16.id, file17.id, file18.id, file19.id, file20.id, file21.id, file22.id, file23.id, file24.id, file25.id]
    }
  }
)

Assistant_ID = assistant.id
print(Assistant_ID)
TELEGRAM_TOKEN = '6832211064:AAGj7DTV_LqZSli9Xz2Yn-0g4oegrg_4aFM'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY,
    thread TEXT
)''')
conn.commit()


# Функция для добавления пользователя в базу данных
async def handle_with_assistant(message, chat_id):
    print('генерация началась')
    cursor.execute('SELECT thread FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    thread_id = result[0] if result is not None else add_user(chat_id)
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
    cursor.execute('SELECT chat_id FROM users WHERE chat_id = ?', (chat_id,))
    thread = client.beta.threads.create()
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (chat_id, thread) VALUES (?, ?)', (chat_id, thread.id))
        conn.commit()
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
