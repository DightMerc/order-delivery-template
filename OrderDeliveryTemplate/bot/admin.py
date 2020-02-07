from django.contrib import admin
from .models import TelegramUser, Product, Settings, Category, Cart, Order, PaySystem, Message, Photo


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegramId', 'username')
    ordering = ('id',)
    search_fields = ('id', 'telegramId', 'username')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'photoUrl', 'fileId')
    ordering = ('id',)
    search_fields = ('id', 'photoUrl', 'fileId')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'number')
    ordering = ('id', 'number',)
    search_fields = ('id', 'title', 'number')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'ru', 'uz', 'active')
    ordering = ('id', 'active',)
    search_fields = ('id', 'ru', 'uz', 'active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'ru', 'uz', 'active')
    ordering = ('id', 'active',)
    search_fields = ('id', 'ru', 'uz', 'active')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'created')
    ordering = ('id', 'active',)
    search_fields = ('id', 'active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')
    ordering = ('id', )
    search_fields = ('id', )


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'token')
    ordering = ('id', )
    search_fields = ('id', 'title', 'token')


@admin.register(PaySystem)
class PaySystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'token')
    ordering = ('id', )
    search_fields = ('id', 'title', 'token')
