from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import TOKEN

bot = Bot(token=(TOKEN))
dp = Dispatcher()
router = Router()
