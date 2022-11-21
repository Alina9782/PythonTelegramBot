from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import sqlite3

from config import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


db = sqlite3.connect('clinic.db')
cursor = db.cursor()


class Reg(StatesGroup):
    date_add = State()
    lastname_add = State()
    firstname_add = State()
    phone_add = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Вітаю в чат-боті для запису на прийом в DermaClinic! "
                        "\nДля перегляду команд, напиши /help")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Команди, які я знаю: \n/create - для створення запису;")


@dp.message_handler(commands=['create'])
async def process_create_command(message: types.Message):
    await message.reply("Створюю запис. \nСкопіюйте потрібний час з запропонованого і відправте. "
                        "\n\nМожна відмінити запис на етапі реєстрації комнадою /cancel")
    await Reg.date_add.set()


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


@dp.message_handler(state=Reg.date_add)
async def process_date_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await message.answer("Внесіть Ваше прізвище.")
    await Reg.lastname_add.set()


@dp.message_handler(state=Reg.lastname_add)
async def process_lastname_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
    await message.answer("Внесіть Ваше ім'я.")
    await Reg.firstname_add.set()


@dp.message_handler(state=Reg.firstname_add)
async def process_firstname_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text
    await message.answer('Внесіть Ваш номер телефону.')
    await Reg.phone_add.set()


@dp.message_handler(state=Reg.phone_add)
async def process_phone_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    cursor.execute(f"UPDATE schedule SET LastName = ('{data['lastname']}') WHERE Time = '{data['date']}'")
    cursor.execute(f"UPDATE schedule SET FirstName = ('{data['firstname']}') WHERE Time = '{data['date']}'")
    cursor.execute(f"UPDATE schedule SET Phone = ('{data['phone']}') WHERE Time = '{data['date']}'")
    db.commit()
    await message.answer('Зареєстровано!')
    await state.finish()


@dp.message_handler()
async def text_message(msg: types.Message):
    await msg.reply("Я тебе не розумію. \nДля перегляду команд, напиши /help")


if __name__ == '__main__':
    executor.start_polling(dp)
