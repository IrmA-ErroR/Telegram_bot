# ТЗ: Необходимо создать бота в телеграме, чтобы после нажатия старт всплывало приветственное сообщение 
#   "<Имя>, привет! Я загадал число от 1 до 10, а ты попробуй его отгадать", после отправки числа пользователем бот должен выдавать угадал пользователь или нет.

import config

import asyncio
from random import randint
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import html


# Создание экземпляра диспетчера
storage = MemoryStorage()  # Хранилище состояний в памяти
bot = Bot(token=config.TOKEN,  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
DB_PATH = 'game_data.db'

# Хранение загаданных чисел для разных пользователей
user_numbers = {}
user_attempts = {}

# Определяем состояния
class GameStates(StatesGroup):
    waiting_for_guess = State()


async def initialize_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                first_time TEXT NOT NULL,
                resent_time TEXT NOT NULL, 
                secret_number INTEGER,
                attempts INTEGER        
            )
        ''')
        await db.commit()

async def add_user(user_id, full_name, username, secret_number, attempts):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.cursor()
        check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        check_user = await check_user.fetchone()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if check_user is None:
            await cursor.execute('''
                INSERT INTO users (user_id, full_name, username, first_time, resent_time, secret_number, attempts)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, full_name, username, current_time, current_time, secret_number, attempts))
        else:
            # Обновление времени последнего обращения
            await cursor.execute('''
                UPDATE users SET resent_time = ? WHERE user_id = ?
            ''', (current_time, user_id))
        await db.commit()


async def update_user(user_id, secret_number, attempts):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.cursor()
        check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        check_user = await check_user.fetchone()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if check_user is None:
            return 'Error'
        else:
            # Обновление времени последнего обращения
            await cursor.execute('''
                UPDATE users SET resent_time = ? , secret_number = ?, attempts = ?                              
                                 WHERE user_id = ?
            ''', (current_time, secret_number, attempts, user_id))
        await db.commit()


@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username

    # Загадать число и сохранить для пользователя
    user_numbers[user_id] = randint(1, 10)
    user_attempts[user_id] = 0
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username, 0, 0)
    await message.answer(f'<b>{html.escape(message.from_user.full_name)}</b>, добро пожаловать!\nЯ загадал число от 1 до 10, а ты попробуй его отгадать')
    await state.set_state(GameStates.waiting_for_guess)


@dp.message(GameStates.waiting_for_guess)
async def guess_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Проверяем, что пользователь начал игру
    if user_id not in user_numbers:
        await message.answer("Пожалуйста, начните игру с помощью команды /start.")
        return

    try:
        guess = int(message.text)
        correct_number = user_numbers[user_id]
        user_attempts[user_id] += 1

        if guess == correct_number:
            await message.answer("Поздравляю, вы угадали число!")
            # Логируем данные в БД
            await update_user(user_id, correct_number, user_attempts[user_id])
            # Удаляем число, чтобы игра не продолжалась
            del user_numbers[user_id]
            del user_attempts[user_id]
            await state.clear()  # Сброс состояния после угадывания
        else:
            await message.answer("Не угадали, попробуйте снова!")
    except ValueError:
        await message.answer("Пожалуйста, введите число от 1 до 10.")

@dp.message()
async def catch_all_handler(message: types.Message):
    await message.answer("Не понял вас.")


async def main() -> None:
  
    await initialize_db()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
