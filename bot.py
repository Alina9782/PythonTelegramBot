from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Вітаю в чат-боті для запису на прийом в DermaClinic! "
                        "\nДля перегляду команд, напиши /help")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Команди, які я знаю: \n/create - для створення запису;")


@dp.message_handler(commands=['create'])
async def process_create_command(msg: types.Message):
    await msg.reply("Створюю запис. \nВаше прізвище?")


@dp.message_handler()
async def text_message(msg: types.Message):
    await msg.reply("Я тебе не розумію. \nДля перегляду команд, напиши /help")


if __name__ == '__main__':
    executor.start_polling(dp)
