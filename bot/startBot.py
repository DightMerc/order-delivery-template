import client
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from messages import Messages
import states
import keyboards

from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile

import os
import aioredis


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                     level=logging.DEBUG)


bot = Bot(token=client.GetToken(), parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(db=7)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    user = message.from_user.id

    if not client.userExsists(user):
        client.userCreate(message.from_user)

    await state.set_data({})

    await states.User.started.set()

    await bot.send_chat_action(user, action="typing")

    text = Messages(user)['start'].replace("{}", message.from_user.first_name)
    markup = keyboards.LanguageKeyboard()
    await bot.send_message(user, text, reply_markup=markup)


@dp.callback_query_handler(state=states.User.started)
async def language_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    client.userSetLanguage(user, data)
    await states.User.main.set()

    await bot.send_chat_action(user, action="typing")

    text = Messages(user)['main']
    markup = keyboards.MenuKeyboard(user)
    await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.main)
async def main_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data in ["ru", "uz"]:
        client.userSetLanguage(user, data)

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['main']
        markup = keyboards.MenuKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)

    elif data == "menu":

        await states.User.menu.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['menu']
        markup = keyboards.CategoriesKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.menu)
async def category_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data == "home":
        await states.User.main.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['main']
        markup = keyboards.MenuKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
    else:
        await states.User.subMenu.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['subMenu']
        markup = keyboards.ProductsKeyboard(user, data)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)

    


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
