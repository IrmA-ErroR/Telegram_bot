import config

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

dp = Dispatcher()

# Клавиатура прикреплена к сообщению (Inline)
@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    kb = [
        [
            types.InlineKeyboardButton(text="Обо мне", callback_data='about_me'),
            types.InlineKeyboardButton(text="О тебе", callback_data='about_you')
        ],
        [types.InlineKeyboardButton(text="Автор", callback_data='author')],
        [types.InlineKeyboardButton(text="Погода", callback_data='weather')],
        [types.InlineKeyboardButton(text="Gismetio", url='https://www.gismeteo.ru')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(
        f'Добрый день, {message.from_user.full_name}\nРад вас видеть',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "about_me")
async def about_me_callback(callback: types.CallbackQuery): # callback.message.edit_text - переписывает сообщение
    await callback.message.edit_text(
        'Рад, что ты спросил\nЯ бот, который присылает прогноз погоды, мама говорит, что я классный'
    )

@dp.callback_query(F.data == 'author')
async def author_handler(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.message.answer(
        f'Моего автора зовут Светлана, \nА меня зовут {(await bot.get_me()).full_name}.'
        f'\nА как тебя зовут? Хотя, можешь не отвечать, я не смогу прочитать'
    )

@dp.callback_query(F.data == 'weather')
async def weather_handler(callback: types.CallbackQuery) -> None:
    await callback.message.answer(
        'Я пока что только учусь, и ещё не знаю, как её смотреть, но скоро здесь будет полный прогноз на день'
    )

@dp.callback_query(F.data == 'about_you')
async def about_you_handler(callback: types.CallbackQuery) -> None:
    await callback.message.answer(f'А тебя зовут {callback.from_user.full_name}!')

# Ответ на другие сообщения
@dp.message()
async def all_handler(message: types.Message) -> None:
    await message.send_copy(chat_id=message.chat.id)
    await message.answer('Мне не знакома эта команда, напишите /start, чтобы узнать мои возможности.')

async def main() -> None:
    token = config.TOKEN
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
