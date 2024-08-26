# Добавление админ-панели бота

## ping: api.telegram.org: Temporary failure in name resolution

import config

import aiosqlite
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from datetime import datetime
from aiogram.types import TelegramObject
from aiogram.filters import BaseFilter

admin_ids = [config.admin_id]

dp = Dispatcher()

class IsAdmin(BaseFilter):
    async def __call__(self, obj: TelegramObject) -> bool:
        return obj.from_user.id in admin_ids


admin_keyboard = [
    [
        types.InlineKeyboardButton(text='Рассылка', callback_data='admin_newsletter'),
        types.InlineKeyboardButton(text='Статистика', callback_data='admin_statistic')
    ],
    [
        types.InlineKeyboardButton(text='Menu', callback_data='admin_menu')
    ]
]
admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard=admin_keyboard)

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

async def get_user_count():
    connect = await aiosqlite.connect('db')
    cursor = await connect.cursor()
    user_count = await cursor.execute('SELECT COUNT(*) FROM users')
    user_count = await user_count.fetchone()
    await cursor.close()
    await connect.close()
    return user_count[0]

@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(f'Добро пожаловать, {message.from_user.full_name}\nРад вас видеть, напишите мне что-нибудь хорошее')

@dp.message(Command('admin'), IsAdmin())
async def admin_command(message: types.Message) -> None:
    await message.answer('Добро пожаловать в Админ-панель!',
                         reply_markup=admin_keyboard)
    
@dp.message(Command('users'), IsAdmin())
async def get_users_command(message: types.Message) -> None:
    users = await get_all_users()
    if users:
        users_list = "\n".join([f"ID: {user[0]}\n\tName: {user[1]}\n\tUsername: {user[2]}\n\tRegistered: {user[3]}\n\tLast seen: {user[4]}" for user in users])
        await message.answer(f"Registered users:\n{users_list}")
    else:
        await message.answer("No users found in the database.")

@dp.callback_query(F.data == 'admin_statistic', IsAdmin())
async def admin_statistic(call: types.CallbackQuery):
    user_count = await get_user_count()
    await call.message.edit_text('Статистика\n\n'
                                 f'Количество пользователей: {user_count}')

# Обработка нажатия кнопки "Menu"
@dp.callback_query(F.data == 'admin_menu', IsAdmin())
async def admin_menu(call: types.CallbackQuery):
    await call.message.edit_text('Вы в админ-меню', reply_markup=admin_keyboard)

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
