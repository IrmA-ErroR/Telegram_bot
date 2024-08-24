# Запись пользрователей в БД
import config

import aiosqlite
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from datetime import datetime

async def initialize_db():
    async with aiosqlite.connect('db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                first_time TEXT NOT NULL,
                resent_time TEXT NOT NULL
            )
        ''')
        await db.commit()


async def add_user(user_id, full_name, username):
    async with aiosqlite.connect('db') as db:
        cursor = await db.cursor()
        check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        check_user = await check_user.fetchone()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if check_user is None:
            await cursor.execute('''
                INSERT INTO users (user_id, full_name, username, first_time, resent_time) 
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, full_name, username, current_time, current_time))
        else:
            # Обновление времени последнего обращения
            await cursor.execute('''
                UPDATE users SET resent_time = ? WHERE user_id = ?
            ''', (current_time, user_id))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect('db') as db:
        cursor = await db.execute('SELECT * FROM users')
        rows = await cursor.fetchall()
        await cursor.close()
    return rows



dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(f'Добро пожаловать, {message.from_user.full_name}\nРад вас видеть, напишите мне что-нибудь хорошее')


@dp.message(Command('users'))
async def get_users_command(message: types.Message) -> None:
    users = await get_all_users()
    if users:
        users_list = "\n".join([f"ID: {user[0]}\n\tName: {user[1]}\n\tUsername: {user[2]}\n\tRegistered: {user[3]}\n\tLast seen: {user[4]}" for user in users])
        await message.answer(f"Registered users:\n{users_list}")
    else:
        await message.answer("No users found in the database.")


# Обработка всех остальных сообщений
@dp.message()
async def catch_all_handler(message: types.Message) -> None:
    await message.answer('Спасибо, Ваше мнение очень важно для нас')

async def main() -> None:
    await initialize_db()  # Инициализация базы данных
    token = config.TOKEN
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
