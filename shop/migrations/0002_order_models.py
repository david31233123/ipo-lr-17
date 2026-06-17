# Generated migration for Order models

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Заказ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('дата_создания', models.DateTimeField(auto_now_add=True)),
                ('дата_обновления', models.DateTimeField(auto_now=True)),
                ('адрес_доставки', models.CharField(max_length=255)),
                ('город', models.CharField(max_length=100)),
                ('почтовый_индекс', models.CharField(max_length=20)),
                ('телефон', models.CharField(max_length=20)),
                ('сумма_заказа', models.DecimalField(decimal_places=2, max_digits=10)),
                ('статус', models.CharField(choices=[('pending', 'В ожидании'), ('processing', 'Обработка'), ('shipped', 'Отправлено'), ('delivered', 'Доставлено'), ('cancelled', 'Отменено')], default='pending', max_length=20)),
                ('примечание', models.TextField(blank=True, null=True)),
                ('пользователь', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='заказы', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-дата_создания'],
            },
        ),
        migrations.CreateModel(
            name='ЭлементЗаказа',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('количество', models.PositiveIntegerField()),
                ('цена_на_момент_заказа', models.DecimalField(decimal_places=2, max_digits=10)),
                ('заказ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='элементы', to='shop.заказ')),
                ('товар', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='элементы_заказа', to='shop.товар')),
            ],
            options={
                'verbose_name': 'Элемент заказа',
                'verbose_name_plural': 'Элементы заказа',
            },
        ),
    ]
