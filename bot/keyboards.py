from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import client


def LanguageKeyboard():

    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('🇷🇺 Русский', callback_data="ru"),
        InlineKeyboardButton('🇺🇿 Ўзбек тили', callback_data="uz")
)


def MenuKeyboard(user, cartCount):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🔍 Меню', callback_data="menu"),
            InlineKeyboardButton('📥 Корзина' if cartCount==0 else f'📥 Корзина ( {cartCount} )', callback_data="cart")
            ).add(
            ).add(InlineKeyboardButton('🌏 О нас', callback_data="about")
            ).add(InlineKeyboardButton('🇺🇿 Ўзбек тили', callback_data="uz"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🔍 Меню', callback_data="menu"),
            InlineKeyboardButton('📥 Корзина' if cartCount==0 else f'📥 Корзина ( {cartCount} )', callback_data="cart")
            ).add(InlineKeyboardButton('🌏 О нас', callback_data="about")
            ).add(InlineKeyboardButton('🇷🇺 Русский', callback_data="ru"))


def PaginationKeyboards(user, current, prevPage, nextPage, count):
    print(f"\n\n{prevPage} {current} {nextPage}\n\n")

    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('⬅️', callback_data=prevPage),
            InlineKeyboardButton(f'{current + 1}/{count}', callback_data="empty"),
            InlineKeyboardButton('➡️', callback_data=nextPage)

            ).add(InlineKeyboardButton('✖️ Убрать из корзины', callback_data=f"clear {current}")
            ).add(InlineKeyboardButton('Сделать заказ', callback_data="order"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('⬅️', callback_data=prevPage),
            InlineKeyboardButton(f'{current + 1}/{count}', callback_data="empty"),
            InlineKeyboardButton('➡️', callback_data=nextPage)

            ).add(InlineKeyboardButton('✖️ Убрать из корзины', callback_data=f"clear {current}")
            ).add(InlineKeyboardButton('Сделать заказ', callback_data="order"))


def CategoriesKeyboard(user):
    lan = client.getUserLanguage(user)
    # lan = user
    buttons = []
    header = []
    footer = []
    footer.append(InlineKeyboardButton('🏡 Назад' if lan == "ru" else "🏡 Ортга", callback_data="home"))

    for category in client.GetCategories():
        buttons.append(InlineKeyboardButton(category.ru if lan == "ru" else category.uz, callback_data=f"{category.id}"))
    return InlineKeyboardMarkup(inline_keyboard=build_products_menu(buttons, 2, header, footer))


def ProductsKeyboard(user, category):
    lan = client.getUserLanguage(user)
    # lan = user
    buttons = []
    header = []
    footer = []
    footer.append(InlineKeyboardButton('🏡 Назад' if lan == "ru" else "🏡 Ортга", callback_data=f"back {category}"))

    for product in client.GetProductsByCatt(category):
        buttons.append(InlineKeyboardButton(product.ru if lan == "ru" else product.uz, callback_data=f"{product.id}"))
    return InlineKeyboardMarkup(inline_keyboard=build_products_menu(buttons, 1, header, footer))


def build_products_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        for btn in footer_buttons:
            menu.append([btn])
    return menu


def CurrentProductKeyboard(user, product, category):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton('📥 Добавить в корзину', callback_data=f"{product}")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data=f"back {category}"))
    else:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton('📥 Добавить в корзину', callback_data=f"{product}")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data=f"back {category}"))


def BackKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().add(InlineKeyboardButton('🏡 Назад', callback_data="back"))
    else:
        return InlineKeyboardMarkup().add(InlineKeyboardButton('🏡 Назад', callback_data="back"))


def ContactKeyboard(user):
    if client.getUserLanguage(user) == "ru":
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отправить свой контакт', request_contact=True)).add(
            KeyboardButton('🏡 Назад'))
    else:
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Телефон рақамингизни юбориш', request_contact=True)).add(
                KeyboardButton('🏡 Ортга'))


def DeliveryKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🙍‍♂️ Самовывоз', callback_data="self"),
            InlineKeyboardButton('🚙 Доставка', callback_data="delivery")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🙍‍♂️ Самовывоз', callback_data="self"),
            InlineKeyboardButton('🚙 Доставка', callback_data="delivery")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))


def TimeKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🕘 В ближайшее время', callback_data="closeTime"),
            InlineKeyboardButton('🕘 Установить время', callback_data="setTime")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🕘 В ближайшее время', callback_data="closeTime"),
            InlineKeyboardButton('🕘 Установить время', callback_data="setTime")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))


def PaymentKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('💵 Наличные', callback_data="cash"),
            InlineKeyboardButton('💳 Оплата картой', callback_data="card")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('💵 Наличные', callback_data="cash"),
            InlineKeyboardButton('💳 Оплата картой', callback_data="card")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))


def PaySystemKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('💳 PayMe', callback_data="payme"),
            InlineKeyboardButton('💳 Click', callback_data="click")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('💳 PayMe', callback_data="payme"),
            InlineKeyboardButton('💳 Click', callback_data="click")
            ).add(InlineKeyboardButton('🏡 Назад', callback_data="back"))


def BuyKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', callback_data='pay')
        ).add(InlineKeyboardButton('🏡 Назад', callback_data='back'))
    else:
        return InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', callback_data='pay')
        ).add(InlineKeyboardButton('🏡 Назад', callback_data='back'))

# if __name__ == "__main__":
#     CategoriesKeyboard('ru')