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

    client.userUpdate(user, language=data)
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
        client.userUpdate(user, language=data)

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

            product = products[0]

            lan = client.getUserLanguage(user)

            if lan=="ru":
                text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
            else:
                text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

            markup = keyboards.PaginationKeyboards(user, 0, products.count() - 1 , 1, products.count())

            file = InputFile.from_url(mediaLink + product.photo.url)
            if client.GetPhotoId(product.photo.url):
                file = client.GetPhotoId(product.photo.url)
                await bot.send_photo(user, file, caption=text, reply_markup=markup)
            else:
                fileId = await bot.send_photo(user, file, caption=text, reply_markup=markup)
                client.SetPhotoId(product.photo.url, fileId.photo[0].file_id)

            await bot.delete_message(user, callback_query.message.message_id)
            
        else:
            await states.User.main.set()
            
            text = Messages(user)['cartEmpty']
            markup = keyboards.MenuKeyboard(user, 0)
            await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.User.cart)
async def category_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    data = callback_query.data


    if str(data).isdigit():
        await bot.answer_callback_query(callback_query.id)

        data = int(data)
        products = client.getCartProducts(user)
        # pagination = Paginator(products, 1)

        product = products[data]
        lan = client.getUserLanguage(user)

        if lan=="ru":
            text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
        else:
            text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

        markup = keyboards.PaginationKeyboards(user,
         data,
         products.count() - 1 if data - 1 == -1 else data - 1 ,
         0 if data + 1 == products.count() else data + 1, 
         products.count()
         )

        file = InputFile.from_url(mediaLink + product.photo.url)
        if client.GetPhotoId(product.photo.url):
            file = client.GetPhotoId(product.photo.url)
            await bot.send_photo(user, file, caption=text, reply_markup=markup)

        await bot.delete_message(user, callback_query.message.message_id)
        
    elif "clear" in str(data):
        current = int(data.replace("clear ", ""))
        products = client.getCartProducts(user)
        product = products[current]

        await bot.answer_callback_query(callback_query.id, Messages(user)['productRemoved'].replace("{}", product.ru if client.getUserLanguage(user)=="ru" else product.uz))

        client.removeFromCart(user, product)

        products = client.getCartProducts(user)

        if products.count()!=0:
            try:
                data = current
                product = products[data]
            except Exception as e:
                data = current - 1
                product = products[data]

            lan = client.getUserLanguage(user)

            if lan=="ru":
                text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
            else:
                text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

            markup = keyboards.PaginationKeyboards(user,
            data,
            products.count() - 1 if data - 1 == -1 else data - 1 ,
            0 if data + 1 == products.count() else data + 1, 
            products.count()
            )

            file = InputFile.from_url(mediaLink + product.photo.url)
            if client.GetPhotoId(product.photo.url):
                file = client.GetPhotoId(product.photo.url)
                await bot.send_photo(user, file, caption=text, reply_markup=markup)

            await bot.delete_message(user, callback_query.message.message_id)
        else:
            await states.User.main.set()

            text = Messages(user)['cartEmpty']
            markup = keyboards.MenuKeyboard(user, 0)
            await bot.send_message(user, text, reply_markup=markup)
            await bot.delete_message(user, callback_query.message.message_id)

    elif data == "empty":
        await bot.answer_callback_query(callback_query.id)

    elif data == "order":
        await states.Order.started.set()

        client.createOrder(user)

        text = Messages(user)['name']
        markup = keyboards.BackKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        await bot.delete_message(user, callback_query.message.message_id)


@dp.message_handler(state=states.Order.started)
async def order_started_command(message: types.Message, state: FSMContext):
    user = message.from_user.id

    name = message.text

    await states.Order.phone.set()

    client.userUpdate(user, realName=name)

    text = Messages(user)['phone']
    markup = keyboards.ContactKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)
    await bot.delete_message(user, message.message_id - 1)


@dp.callback_query_handler(state=states.Order.started)
async def back_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    await states.User.cart.set()

    await bot.send_chat_action(user, action="typing")

    products = client.getCartProducts(user)
    if products:

        product = products[0]

        lan = client.getUserLanguage(user)

        if lan=="ru":
            text = Messages(user)['descriptionProduct'].format(product.ru, product.ruDescription, product.price)
        else:
            text = Messages(user)['descriptionProduct'].format(product.uz, product.uzDescription, product.price)

        markup = keyboards.PaginationKeyboards(user, 0, products.count() - 1 , 1, products.count())

        file = InputFile.from_url(mediaLink + product.photo.url)
        if client.GetPhotoId(product.photo.url):
            file = client.GetPhotoId(product.photo.url)
            await bot.send_photo(user, file, caption=text, reply_markup=markup)
        else:
            fileId = await bot.send_photo(user, file, caption=text, reply_markup=markup)
            client.SetPhotoId(product.photo.url, fileId.photo[0].file_id)

        await bot.delete_message(user, callback_query.message.message_id)


@dp.message_handler(state=states.Order.phone, content_types=types.ContentType.CONTACT)
async def user_contact_handler(message: types.Message, state: FSMContext):

    user = message.from_user.id

    phone = str(message.contact.phone_number)

    client.userUpdate(user, phone=phone.replace("+", ""))

    await states.Order.delivery.set()

    text = Messages(user)['delivery']
    markup = keyboards.DeliveryKeyboard(user)
    await bot.send_message(user, text, reply_markup=markup)
    await bot.delete_message(user, message.message_id - 1)




@dp.callback_query_handler(state=states.Order.delivery)
async def delivery_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data == "back":
        await states.Order.phone.set()

        text = Messages(user)['phone']
        markup = keyboards.ContactKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        await bot.delete_message(user, callback_query.message.message_id)

    elif data == "self":
        await states.Order.selfOut.set()

        await bot.send_chat_action(user, action="typing")

        client.updateOrder(user, delivery=False)

        text = Messages(user)["outTime"]
        markup = keyboards.TimeKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.Order.selfOut)
async def selfout_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data == "back":
        await states.Order.delivery.set()

        text = Messages(user)['delivery']
        markup = keyboards.DeliveryKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
        

    elif data == "closeTime":
        await states.Order.closeTime.set()

        await bot.send_chat_action(user, action="typing")

        client.updateOrder(user, time="Ближайшее время")

        text = Messages(user)["payment"]
        markup = keyboards.PaymentKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)

    elif data == "setTime":
        await states.Order.setTime.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)["setTime"]
        markup = keyboards.BackKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.Order.closeTime)
async def closeTime_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data == "back":
        await states.Order.selfOut.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)["outTime"]
        markup = keyboards.TimeKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
    elif data == "cash":
        await states.User.main.set()

        await bot.send_chat_action(user, action="typing")

        client.updateOrder(user, cash=True)

        text = Messages(user)['main']
        markup = keyboards.MenuKeyboard(user, client.getCartCount(user))
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)

    elif data == "card":
        await states.Order.card.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)['choosePaySystem']
        markup = keyboards.PaySystemKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(state=states.Order.card)
async def card_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    data = callback_query.data

    await bot.answer_callback_query(callback_query.id)

    if data == "back":
        await states.Order.closeTime.set()

        await bot.send_chat_action(user, action="typing")

        text = Messages(user)["payment"]
        markup = keyboards.PaymentKeyboard(user)
        await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
    elif data in ["payme", "click"]:
        await states.Order.pay.set()

        await bot.send_chat_action(user, action="typing")

        if data == "click":
            client.updateOrder(user, click=True)
            token = GetPaymentToken("Click Test")

        else:
            client.updateOrder(user, payme=True)
            token = client.GetPaymentToken("PayMe Test")

        text = "Some Shit"

        price = 100000
        prices = [
            types.LabeledPrice(label=text, amount=price * 100),
        ]
        await states.Order.preCheckout.set()

        await bot.send_invoice(user, title='TRATATA',
                            description=text,
                            provider_token=token,
                            currency='uzs',
                            photo_url='https://telegra.ph/file/e90f7d3f8bc360f7fb731.png',
                            photo_height=512,  # !=0/None or picture won't be shown
                            photo_width=512,
                            photo_size=512,
                            is_flexible=False,  # True If you need to set up Shipping Fee
                            prices=prices,
                            #    need_shipping_address=True,
                                # need_email=True,
                                # need_name=True,
                                # need_phone_number=True,
                            start_parameter='cinema-system-payment',
                            payload='HAPPY FRIDAYS COUPON')

        await bot.delete_message(user, callback_query.message.message_id)


        # text = Messages(user)["pay"]
        # markup = keyboards.BuyKeyboard(user)
        # await bot.edit_message_text(text, user, callback_query.message.message_id, reply_markup=markup)
        
    


@dp.message_handler(state=states.Order.phone)
async def order_started_command(message: types.Message, state: FSMContext):
    user = message.from_user.id

    text = message.text

    if text in ["🏡 Назад", "🏡 Ортга"]:
        await states.Order.started.set()

        client.createOrder(user)

        text = Messages(user)['name']
        markup = keyboards.BackKeyboard(user)
        await bot.send_message(user, text, reply_markup=markup)
        await bot.delete_message(user, message.message_id-1)

    
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
