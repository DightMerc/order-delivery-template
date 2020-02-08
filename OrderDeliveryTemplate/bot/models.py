from django.db import models
from django.utils import timezone


class Photo(models.Model):

    photoUrl = models.CharField("url", max_length=512)
    fileId = models.CharField("fileId", max_length=256, null=True, blank=True)


class Product(models.Model):
    ru = models.CharField("Название на русском", max_length=256)
    uz = models.CharField("Название на узбекском", max_length=256)

    ruDescription = models.TextField("Описание на русском", max_length=256)
    uzDescription = models.TextField("Описание на узбекском", max_length=256)

    photo = models.ImageField("Фото", upload_to="media/common/")

    active = models.BooleanField("Статус активности", default=True)

    price = models.PositiveIntegerField("Цена")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.id} {self.ru}"


class Category(models.Model):
    ru = models.CharField("Название на русском", max_length=256)
    uz = models.CharField("Название на узбекском", max_length=256)

    products = models.ManyToManyField(Product)

    active = models.BooleanField("Статус активности", default=True)

    photo = models.ImageField("Фото", upload_to="media/common/")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.id} {self.ru}"


class TelegramUser(models.Model):
    telegramId = models.PositiveIntegerField("ID Telegram")

    phone = models.PositiveIntegerField("Номер телефона", null=True, blank=True)
    username = models.CharField("Username", max_length=256)

    language = models.CharField("Язык", max_length=5, default="ru")
    full_name = models.CharField("Имя в телеграм", max_length=255, default="", null=False)

    readlName = models.CharField("Имя", max_length=255, default="", null=True, blank=True)

    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.id} {self.telegramId}"


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product)

    created = models.DateTimeField("Дата создания заказа", default=timezone.now, null=False, blank=False)

    active = models.BooleanField("Статус активности", default=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.id} {self.user}"


class Order(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    created = models.DateTimeField("Дата создания заказа", default=timezone.now, null=False, blank=False)

    delivery = models.BooleanField("Статус активности", default=True)

    geoX = models.IntegerField("Локация X", null=True, blank=True)
    geoY = models.IntegerField("Локация X", null=True, blank=True)

    time = models.CharField("Время", max_length=256, null=False, blank=False)

    click = models.BooleanField("Оплачено Click", default=True)
    payMe = models.BooleanField("Оплачено PayMe", default=True)
    cash = models.BooleanField("Оплачено наличными", default=True)

    active = models.BooleanField("Подтвержден", default=True)

    activated = models.DateTimeField("Дата подтверждения заказа", default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    title = models.CharField("Название", max_length=256)
    number = models.PositiveIntegerField("Порядковый номер")

    ru = models.TextField("Текст на русском")
    uz = models.TextField("Текст на узбекском")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.id} {self.title}"


class PaySystem(models.Model):
    title = models.CharField("Название", max_length=256)

    token = models.CharField("Токен", max_length=256)

    class Meta:
        verbose_name = "Платежная система"
        verbose_name_plural = "Платежные системы"

    def __str__(self):
        return f"{self.id} {self.title}"


class Settings(models.Model):
    title = models.CharField("Название", max_length=256)

    token = models.CharField("Токен бота", max_length=256)
    paySystem = models.ManyToManyField(PaySystem)

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return f"{self.id} {self.title}"