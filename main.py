import kb as kb
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.types import ParseMode, ReplyKeyboardMarkup, message
from utils import Form
from aiogram.dispatcher import FSMContext
import logging
from utils import get_currency, weatheer
import aiogram.utils.markdown as md
import asyncio
import json

import aiohttp



from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='weather')
async def wether(message: types.Message):
    keyboard_markup= types.ReplyKeyboardMarkup(row_width=3)
    button_text= ('Казань', 'Уфа', 'Москва', "Санкт-Петербург")
    keyboard_markup.row(*(types.KeyboardButton(text)for text in button_text))
    await message.reply('Выберите город', reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    # Set state
    await Form.name.set()

    await message.reply("Hi there! What's your name?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it

    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())



#@dp.message_handler()
#async def currency(message: types.Message):
 #   await message.reply (str(await get_currency(message.text)))
@dp.message_handler()
async def weather(message: types.Message):
    s = message.text

    await message.reply(str(await weatheer(s)))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)