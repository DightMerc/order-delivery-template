from django.db import models


class TelegramUser(models.Model):
    telegramId = models.PositiveIntegerField("ID Telegram")

    phone = models.PositiveIntegerField("Номер телефона")
    username = models.CharField("Username")

    def __str__(self):
        return f"{self.id} {self.telegramId}"


class Message(models.Model):
    title = models.CharField("Название")
    number = models.PositiveIntegerField("Порядковый номер")

    ru = models.TextField("Текст на русском")
    uz = models.TextField("Текст на узбекском")

    def __str__(self):
        return f"{self.id} {self.title}"


class PaySystem(models.Model):
    title = models.CharField("Название")
    
    token = models.CharField("Токен")

    def __str__(self):
        return f"{self.id} {self.title}"


class Settings(models.Model):
    title = models.CharField("Название")

    token = models.CharField("Токен бота")
    paySystem = models.ManyToMany(PaySystem)

    def __str__(self):
        return f"{self.id} {self.title}"