import os, sys
import django
from django.shortcuts import get_object_or_404
import shutil


proj_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] + "/OrderDeliveryTemplate/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OrderDeliveryTemplate.settings")
sys.path.append(proj_path)

print(proj_path)
django.setup()


from bot import models as bot_models


def GetToken():
    return bot_models.Settings.objects.get(pk=1).token


def getUserLanguage(user):
    return str(bot_models.TelegramUser.objects.get(telegramId=int(user)).language)


def getMessage(number, lan):
    if lan == "uz":
        return bot_models.Message.objects.get(number=number).uz
    else:
        return bot_models.Message.objects.get(number=number).ru


def getRegions(main):
    return bot_models.Region.objects.all().filter(regionOwner=bot_models.MainRegion.objects.get(title=main).id)


def userExsists(user):
    try:
        bot_models.TelegramUser.objects.get(telegramId=int(user))
        return True
    except Exception as e:
        return False


def userCreate(user):
    new_user = bot_models.TelegramUser()

    new_user.telegramId = user.id
    new_user.full_name = user.full_name
    new_user.username = user.username

    new_user.save()

    return True


def getUser(user):
    try:
        user = bot_models.TelegramUser.objects.get(telegramId=int(user))
        return user
    except Exception as identifier:
        return False


def userSetLanguage(user, language):

    current_user = bot_models.TelegramUser.objects.get(telegramId=int(user))
    current_user.language = language

    current_user.save()


def GetCategories():

    return bot_models.Category.objects.filter(active=True)


def GetProductsByCatt(category):

    return bot_models.Category.objects.get(pk=category).products.all()


def GetProduct(product):

    return bot_models.Product.objects.get(pk=product)


def SetPhotoId(url, id):

    if bot_models.Photo.objects.filter(photoUrl=url).count() != 0:
        if photo == bot_models.Photo.objects.get(photoUrl=url).fileId != None:
            return photo.fileId
        else:
            photo.fileId = id
            photo.save()

            return id
    else:
        photo = bot_models.Photo()
        photo.fileId = id
        photo.photoUrl = url
        photo.save()


def GetPhotoId(url):
    try:
        id = bot_models.Photo.objects.get(photoUrl=url).fileId
        return id
    except Exception as e:
        return False


def addToCart(user, product):
    user = bot_models.TelegramUser.objects.get(telegramId=user)

    if bot_models.Cart.objects.filter(user=user, active=True).count()!=0:
        cart = bot_models.Cart.objects.filter(active=True).get(user=user)
        cart.products.add(product)
    else:
        cart = bot_models.Cart()
        cart.user = user
        cart.active = True
        cart.save()

        cart.products.add(product)

    return True


def getCartCount(user):
    user = bot_models.TelegramUser.objects.get(telegramId=user)

    if bot_models.Cart.objects.filter(user=user, active=True).count()!=0:
        return bot_models.Cart.objects.filter(active=True).get(user=user).products.all().count()
    else:
        return 0


def getCartProducts(user):
    user = bot_models.TelegramUser.objects.get(telegramId=user)

    if bot_models.Cart.objects.filter(user=user, active=True).count()!=0:
        return bot_models.Cart.objects.filter(active=True).get(user=user).products.all()
    else:
        return False