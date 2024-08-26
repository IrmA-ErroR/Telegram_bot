import config

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    await message.answer(f'Добрый вечер, {message.from_user.full_name}\nРад вас видеть, напишите Меню, чтобы узнать мои команды')

# Обработка сообщений с фотографиями
@dp.message(F.photo)
async def photo_handler(message: types.Message) -> None:
    # Получаем файл фото
    photo_id = message.photo[-1].file_id  # Берем последнее фото (оно будет в наилучшем разрешении)
    print(photo_id)
    await message.answer_photo(photo_id, caption="Вот ваше фото!")

# Обработка сообщений с документами
@dp.message(F.document)
async def document_handler(message: types.Message) -> None:
    document_id = message.document.file_id
    print(document_id)
    await message.answer_document(document_id, caption="Вот ваш документ!")


# Отправляем аватарку
@dp.message(F.text == 'аватарка')
async def send_photo(message: types.Message):
    photo_id = 'AgACAgIAAxkBAAO5ZsitM5akhDy8FIRIAgzgjagjl5YAAtnkMRt0vEhKN3zdbqPnHUABAAMCAAN5AAM1BA'
    await message.answer_photo(photo_id)

# Обработка всех остальных сообщений
@dp.message()
async def catch_all_handler(message: types.Message) -> None:
    await message.answer('Я ловлю всех и вся, но мне нужны фото или документы!')

async def main() -> None:
    token = config.TOKEN
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
