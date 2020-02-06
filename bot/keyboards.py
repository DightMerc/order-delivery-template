from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import client


def LanguageKeyboard():

    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('🇷🇺 Русский', callback_data="ru"),
        InlineKeyboardButton('🇺🇿 Ўзбек тили', callback_data="uz")
)


def MenuKeyboard(user):
    lan = client.getUserLanguage(user)
    if lan == "ru":
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🔍 Меню', callback_data="menu"),
            InlineKeyboardButton('📥 Корзина', callback_data="cart")
            ).add(
            ).add(InlineKeyboardButton('🌏 О нас', callback_data="about")
            ).add(InlineKeyboardButton('🇺🇿 Ўзбек тили', callback_data="uz"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('🔍 Меню', callback_data="menu"),
            InlineKeyboardButton('📥 Корзина', callback_data="cart")
            ).add(InlineKeyboardButton('🌏 О нас', callback_data="about")
            ).add(InlineKeyboardButton('🇷🇺 Русский', callback_data="ru"))


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
    footer.append(InlineKeyboardButton('🏡 Назад' if lan == "ru" else "🏡 Ортга", callback_data="home"))

    for product in client.GetProductsByCatt(category):
        buttons.append(InlineKeyboardButton(product.ru if lan == "ru" else product.uz, callback_data=f"{product.id}"))
    return InlineKeyboardMarkup(inline_keyboard=build_products_menu(buttons, 2, header, footer))


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


# if __name__ == "__main__":
#     CategoriesKeyboard('ru')