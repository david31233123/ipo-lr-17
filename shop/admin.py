from django.contrib import admin
from .models import Категория, Производитель, Товар, Корзина, ЭлементКорзины


@admin.register(Категория)
class КатегорияAdmin(admin.ModelAdmin):
    list_display = ('название',)
    search_fields = ('название',)


@admin.register(Производитель)
class ПроизводительAdmin(admin.ModelAdmin):
    list_display = ('название', 'страна')
    list_filter = ('страна',)
    search_fields = ('название', 'страна')


@admin.register(Товар)
class ТоварAdmin(admin.ModelAdmin):
    list_display = ('название', 'цена', 'количество_на_складе', 'категория', 'производитель')
    list_filter = ('категория', 'производитель')
    search_fields = ('название', 'описание')
    list_editable = ('цена', 'количество_на_складе')


@admin.register(Корзина)
class КорзинаAdmin(admin.ModelAdmin):
    list_display = ('пользователь', 'дата_создания', 'общая_стоимость')
    list_filter = ('дата_создания',)


@admin.register(ЭлементКорзины)
class ЭлементКорзиныAdmin(admin.ModelAdmin):
    list_display = ('товар', 'корзина', 'количество', 'стоимость_элемента')
    list_filter = ('корзина',)
