from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
