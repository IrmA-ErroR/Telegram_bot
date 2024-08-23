##### Отработка меню бота
import config

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

dp = Dispatcher()

# Клавиатура внизу (где поле сообщения)
@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Обо мне"),
            types.KeyboardButton(text="О тебе")
         ],
        [types.KeyboardButton(text="Автор")],
        [types.KeyboardButton(text="Погода")]
        
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f'Добрый день, {message.from_user.full_name}\n'
                         f'Рад вас видеть', reply_markup=keyboard)


# # Текстовое меню команд
# @dp.message(Command('start'))
# async def start_command(message: types.Message) -> None:
#     await message.answer(f'Добрый день, {message.from_user.full_name}\n'
#                          f'Рад вас видеть, напишите Меню, чтобы узнать мои команды')


@dp.message(Command('menu'))
async def menu_handler(message: types.Message) -> None:
    await message.answer('Мои команды\n\n'
                         'Обо мне - я расскажуо себе \n'
                         'Автор - я назову имя моего создателя\n'
                         'Погода - я скажу прогноз погоды\n'
                         'О тебе - я расскажу всё, что знаю о тебе')


@dp.message(F.text == 'Обо мне')
async def about_me_handler(message: types.Message) -> None:
    await message.answer('Рад, что ты спросил\n'
                         'Я бот, который присылает прогноз погоды, мама говорит, что я классный')


@dp.message(F.text == 'Автор')
async def name_handler(message: types.Message, bot: Bot) -> None:
    await message.answer(f'Моего автора зовут Светлана, \nА меня зовут {(await bot.get_me()).full_name}. '
                         f'\nА как тебя зовут? Хотя, можешь не отвечать, я не смогу прочитать')


@dp.message(F.text == 'Погода')
async def portfolio_handler(message: types.Message) -> None:
    await message.answer('Я пока что только учусь, и ещё не знаю как её смотреть, но скоро здесь будет полный прогноз на день')


@dp.message(F.text == 'О тебе')
async def about_you_handler(message: types.Message) -> None:
    await message.answer(f'А тебя зовут {message.from_user.full_name}!')

# Ответ на другие сообщения
@dp.message()
async def all_handler(message: types.Message) -> None:
    await message.send_copy(chat_id=message.chat.id)
    await message.answer('Мне не знакома эта команда, напишите Меню, чтобы узнать мои возможности')
    



async def main() -> None:
    token = config.TOKEN
    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())