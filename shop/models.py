from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# ==================== Задание 1 ====================

class Категория(models.Model):
    """Модель категории товара"""
    название = models.CharField(max_length=100)
    описание = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.название


class Производитель(models.Model):
    """Модель производителя"""
    название = models.CharField(max_length=100)
    страна = models.CharField(max_length=100)
    описание = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.название


class Товар(models.Model):
    """Модель товара"""
    название = models.CharField(max_length=200)
    описание = models.TextField()
    фото_товара = models.ImageField(upload_to='products/', blank=True, null=True)
    цена = models.DecimalField(max_digits=10, decimal_places=2)
    количество_на_складе = models.IntegerField()
    категория = models.ForeignKey(Категория, on_delete=models.CASCADE, related_name='товары')
    производитель = models.ForeignKey(Производитель, on_delete=models.CASCADE, related_name='товары')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.название

    def clean(self):
        """Валидация: цена и количество не могут быть отрицательными"""
        if self.цена < 0:
            raise ValidationError({'цена': 'Цена не может быть отрицательной'})
        if self.количество_на_складе < 0:
            raise ValidationError({'количество_на_складе': 'Количество на складе не может быть отрицательным'})


# ==================== Задание 2 ====================

class Корзина(models.Model):
    """Модель корзины пользователя"""
    пользователь = models.OneToOneField(User, on_delete=models.CASCADE, related_name='корзина')
    дата_создания = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина пользователя {self.пользователь.username}"

    def общая_стоимость(self):
        """Вычисляет сумму стоимости всех элементов корзины"""
        элементы = self.элементы.all()
        return sum(элемент.стоимость_элемента() for элемент in элементы)


class ЭлементКорзины(models.Model):
    """Модель элемента корзины"""
    корзина = models.ForeignKey(Корзина, on_delete=models.CASCADE, related_name='элементы')
    товар = models.ForeignKey(Товар, on_delete=models.CASCADE, related_name='элементы_корзины')
    количество = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f"{self.товар.название} ({self.количество} шт.)"

    def стоимость_элемента(self):
        """Возвращает стоимость элемента (цена товара * количество)"""
        return self.товар.цена * self.количество

    def clean(self):
        """Валидация: количество не должно превышать количество на складе"""
        if self.количество > self.товар.количество_на_складе:
            raise ValidationError({
                'количество': f'Количество не может превышать {self.товар.количество_на_складе} (доступно на складе)'
            })
