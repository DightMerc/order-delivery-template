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
            InlineKeyboardButton(f'{current}/{count}', callback_data="empty"),
            InlineKeyboardButton('➡️', callback_data=nextPage)

            ).add(InlineKeyboardButton('✖️ Убрать из корзины', callback_data="clear")
            ).add(InlineKeyboardButton('Сделать заказ', callback_data="order"))
    else:
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton('⬅️', callback_data=prevPage),
            InlineKeyboardButton(f'{current}/{count}', callback_data="empty"),
            InlineKeyboardButton('➡️', callback_data=nextPage)

            ).add(InlineKeyboardButton('✖️ Убрать из корзины', callback_data="clear")
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

# if __name__ == "__main__":
#     CategoriesKeyboard('ru')