from django.db import models
from django.utils import timezone


class Product(models.Model):
    ru = models.CharField("Название на русском", max_length=256)
    uz = models.CharField("Название на узбекском", max_length=256)

    ruDescription = models.TextField("Описание на русском", max_length=256)
    uzDescription = models.TextField("Описание на узбекском", max_length=256)

    photo = models.ImageField("Фото", upload_to="media/common/")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.id} {self.ru}"


class Category(models.Model):
    ru = models.CharField("Название на русском", max_length=256)
    uz = models.CharField("Название на узбекском", max_length=256)

    products = models.ManyToManyField(Product)

    photo = models.ImageField("Фото", upload_to="media/common/")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.id} {self.ru}"


class TelegramUser(models.Model):
    telegramId = models.PositiveIntegerField("ID Telegram")

    phone = models.PositiveIntegerField("Номер телефона")
    username = models.CharField("Username", max_length=256)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.id} {self.telegramId}"


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product)

    created = models.DateTimeField("Дата создания заказа", default=timezone.now, null=False, blank=False)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.id} {self.ru}"


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