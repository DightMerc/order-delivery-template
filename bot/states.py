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
    phone = State()
    delivery = State()
    selfOut = State()
    deliveryOut = State()
    closeTime = State()
    setTime = State()
    card = State()
    pay = State()
    preCheckout = State()
    
