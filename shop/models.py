from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    @property
    def placeholder_image(self):
        placeholder_images = [
            'images/boardgame-1.svg',
            'images/boardgame-2.svg',
            'images/boardgame-3.svg',
            'images/boardgame-4.svg',
            'images/boardgame-5.svg',
            'images/boardgame-6.svg',
        ]
        if not self.pk:
            return placeholder_images[0]
        return placeholder_images[(self.pk - 1) % len(placeholder_images)]

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


class Profile(models.Model):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Покупатель'
        ADMIN = 'ADMIN', 'Администратор'
        MANAGER = 'MANAGER', 'Менеджер'

    пользователь = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    full_name = models.CharField('ФИО', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес доставки', blank=True)
    favorite_category = models.ForeignKey(Категория, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_by')
    city = models.CharField('Город', max_length=100, blank=True)
    postal_code = models.CharField('Почтовый индекс', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.пользователь.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(пользователь=instance)


# ==================== Задание 3: Модель Заказа ====================

class Заказ(models.Model):
    """Модель заказа пользователя"""
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'Обработка'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    ]
    
    пользователь = models.ForeignKey(User, on_delete=models.CASCADE, related_name='заказы')
    дата_создания = models.DateTimeField(auto_now_add=True)
    дата_обновления = models.DateTimeField(auto_now=True)
    
    # Данные доставки
    адрес_доставки = models.CharField(max_length=255)
    город = models.CharField(max_length=100)
    почтовый_индекс = models.CharField(max_length=20)
    телефон = models.CharField(max_length=20)
    
    # Сумма и статус
    сумма_заказа = models.DecimalField(max_digits=10, decimal_places=2)
    статус = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    примечание = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-дата_создания']
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.пользователь.username}"


class ЭлементЗаказа(models.Model):
    """Модель элемента заказа"""
    заказ = models.ForeignKey(Заказ, on_delete=models.CASCADE, related_name='элементы')
    товар = models.ForeignKey(Товар, on_delete=models.CASCADE, related_name='элементы_заказа')
    количество = models.PositiveIntegerField()
    цена_на_момент_заказа = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.товар.название} ({self.количество} шт.)"
    
    def стоимость(self):
        """Возвращает стоимость элемента заказа"""
        return self.цена_на_момент_заказа * self.количество
