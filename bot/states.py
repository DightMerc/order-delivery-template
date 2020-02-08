from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    started = State() 
    main = State()
    menu = State() 
    subMenu = State()
    productShow = State()
    cart = State()


class Order(StatesGroup):
    started = State() 
