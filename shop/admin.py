from django.contrib import admin
from .models import (
    Категория, Производитель, Товар, Корзина, ЭлементКорзины,
    Заказ, ЭлементЗаказа
)


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


class ЭлементЗаказаInline(admin.TabularInline):
    """Встроенное редактирование элементов заказа"""
    model = ЭлементЗаказа
    extra = 0
    readonly_fields = ('товар', 'количество', 'цена_на_момент_заказа', 'стоимость')
    fields = ('товар', 'количество', 'цена_на_момент_заказа', 'стоимость')

    def стоимость(self, obj):
        return f"{obj.стоимость()} ₽"
    стоимость.short_description = 'Стоимость'


@admin.register(Заказ)
class ЗаказAdmin(admin.ModelAdmin):
    list_display = ('id', 'пользователь', 'сумма_заказа', 'статус', 'дата_создания')
    list_filter = ('статус', 'дата_создания')
    search_fields = ('пользователь__username', 'адрес_доставки', 'город')
    readonly_fields = ('пользователь', 'дата_создания', 'дата_обновления', 'сумма_заказа')
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('пользователь', 'дата_создания', 'дата_обновления', 'сумма_заказа', 'статус')
        }),
        ('Адрес доставки', {
            'fields': ('адрес_доставки', 'город', 'почтовый_индекс', 'телефон')
        }),
        ('Примечания', {
            'fields': ('примечание',)
        }),
    )
    inlines = [ЭлементЗаказаInline]


@admin.register(ЭлементЗаказа)
class ЭлементЗаказаAdmin(admin.ModelAdmin):
    list_display = ('заказ', 'товар', 'количество', 'цена_на_момент_заказа', 'стоимость')
    list_filter = ('заказ', 'товар')
    readonly_fields = ('заказ', 'товар', 'количество', 'цена_на_момент_заказа')
