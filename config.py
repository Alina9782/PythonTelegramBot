from aiogram.dispatcher.filters.state import StatesGroup, State

TOKEN = '5865637947:AAHUvnA6WRofEU2i2eZc5DF4m_n9VCDitHA'


class Reg(StatesGroup):
    date_add = State()
    lastname_add = State()
    firstname_add = State()
    phone_add = State()


class GetSchedule(StatesGroup):
    date_add = State()
