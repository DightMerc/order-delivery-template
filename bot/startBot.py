import client
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from django.core.paginator import Paginator


from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from messages import Messages
import states
import keyboards

from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile, InputMedia

import os
import aioredis


mediaLink = "http://127.0.0.1:8000/"


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
    markup = keyboards.MenuKeyboard(user, client.getCartCount(user))
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
        markup = keyboards.MenuKeyboard(user, client.getCartCount(user))
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)

    elif data == "menu":

        await states.User.menu.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['menu']
        markup = keyboards.CategoriesKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
    elif data == "cart":

        await states.User.cart.set()

        await bot.send_chat_action(user, action="typing")

        products = client.getCartProducts(user)
        if products:
            pagination = Paginator(products, 1)

            product = pagination.get_page(1)[0]

            lan = client.getUserLanguage(user)

            if lan=="ru":
                text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
            else:
                text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

            markup = keyboards.PaginationKeyboards(user, 1, pagination.num_pages, 2, pagination.num_pages)

            file = InputFile.from_url(mediaLink + product.photo.url)
            if client.GetPhotoId(product.photo.url):
                file = client.GetPhotoId(product.photo.url)
                await bot.send_photo(user, file, caption=text, reply_markup=markup)
            else:
                fileId = await bot.send_photo(user, file, caption=text, reply_markup=markup)
                client.SetPhotoId(product.photo.url, fileId.photo[0].file_id)

            await bot.delete_message(user, callback_query.message.message_id)
            
        else:
            text = Messages(user)['cartEmpty']
            markup = keyboards.CategoriesKeyboard(user)
            await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


# @dp.callback_query_handler(state=states.User.cart)
# async def category_handler(callback_query: types.CallbackQuery, state: FSMContext):
#     user = callback_query.from_user.id

#     data = callback_query.data

#     await bot.answer_callback_query(callback_query.id)

#     if str(data).isdigit():
#         data = int(data) - 1
#         products = client.getCartProducts(user)
#         # pagination = Paginator(products, 1)

#         product = products[data]
#         lan = client.getUserLanguage(user)

#         if lan=="ru":
#             text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
#         else:
#             text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

#         markup = keyboards.PaginationKeyboards(user,
#          data,
#          products.count() if data - 1 != 0 else data - 1 ,
#          1 if data + 1 != products.count() else data + 1, 
#          products.count()
#          )

#         file = InputFile.from_url(mediaLink + product.photo.url)
#         if client.GetPhotoId(product.photo.url):
#             file = client.GetPhotoId(product.photo.url)
#             await bot.send_photo(user, file, caption=text, reply_markup=markup)

#         await bot.delete_message(user, callback_query.message.message_id)


@dp.callback_query_handler(state=states.User.menu)
async def category_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data == "home":
        await states.User.main.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['main']
        markup = keyboards.MenuKeyboard(user, client.getCartCount(user))
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
    else:
        await states.User.subMenu.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['subMenu']
        markup = keyboards.ProductsKeyboard(user, data)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.subMenu)
async def subMenu_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if "back" in data:
        await states.User.menu.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['menu']
        markup = keyboards.CategoriesKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
    else:
        await states.User.productShow.set()

        await bot.send_chat_action(user, action="typing")
    
        
        product = client.GetProduct(data)
        category = client.bot_models.Category.objects.filter(products__id=product.id).first()

        lan = client.getUserLanguage(user)

        if lan=="ru":
            text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
        else:
            text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

        markup = keyboards.CurrentProductKeyboard(user, product.id, category.id)

        file = InputFile.from_url(mediaLink + product.photo.url)
        if client.GetPhotoId(product.photo.url):
            file = client.GetPhotoId(product.photo.url)
            print(f"\n\n{file}\n\n")
            await bot.send_photo(user, file, caption=text, reply_markup=markup)
        else:
            fileId = await bot.send_photo(user, file, caption=text, reply_markup=markup)
            client.SetPhotoId(product.photo.url, fileId.photo[0].file_id)

        await bot.delete_message(user, callback_query.message.message_id)
        

@dp.callback_query_handler(state=states.User.productShow)
async def productShow_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data


    if "back" in data:

        await bot.answer_callback_query(callback_query.id)

        await states.User.subMenu.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['subMenu']
        markup = keyboards.ProductsKeyboard(user, data.replace("back ",""))
        await bot.send_message(user, text, reply_markup=markup)
        await bot.delete_message(user, callback_query.message.message_id)
    else:

        product = client.GetProduct(data)

        client.addToCart(user, product)

        await states.User.main.set()

        await bot.send_chat_action(user, action="typing")
        await bot.answer_callback_query(callback_query.id, Messages(user)['productAdded'].replace("{}", product.ru if client.getUserLanguage(user)=="ru" else product.uz))

        text = Messages(user)['main']
        markup = keyboards.MenuKeyboard(user, client.getCartCount(user))
        await bot.send_message(user, text, reply_markup=markup)
        await bot.delete_message(user, callback_query.message.message_id)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
