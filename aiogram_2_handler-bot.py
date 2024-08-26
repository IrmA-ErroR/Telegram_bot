##### Bot с обработкой сообщений (handler)
## В наилучшем варианте порядок регистрации хендлеров не должен иметь никакого значения
import config

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    await message.answer(f'Добрый вечер, {message.from_user.full_name}\nРад вас видеть, напишите Меню, чтобы узнать мои команды')

@dp.message(F.text == 'Меню')
async def menu_handler(message: types.Message) -> None:
    await message.answer('Мои команды\n\nПривет - я тебе отвечу привет!\nЧай - я расскажу о вкусном чае')

@dp.message(F.text == 'Привет')
async def hello_handler(message: types.Message) -> None:
    await message.answer('Привет! Как у тебя дела?')

@dp.message(F.text == 'Чай')
async def morse_handler(message: types.Message) -> None:
    await message.answer('Ты не представляешь какой вкусный чай я сегодня пил. Мне кажется, он вызывает зависимость')

# Может перехватить все сообщения, но таких handler лучше избегать
@dp.message()
async def all_handler(message: types.Message) -> None:
    await message.answer('Я ловлю всех и вся')

async def main() -> None:
    token = config.TOKEN
    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())