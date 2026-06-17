from rest_framework import serializers

from .models import (
    Товар, Категория, Производитель, Корзина, ЭлементКорзины,
    Profile, Заказ, ЭлементЗаказа
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Категория
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Производитель
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    фото_товара = serializers.SerializerMethodField()

    class Meta:
        model = Товар
        fields = '__all__'

    def get_фото_товара(self, obj):
        if obj.фото_товара:
            return obj.фото_товара.url
        return None


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='пользователь.username', read_only=True)
    email = serializers.EmailField(source='пользователь.email', required=False)
    favorite_category = serializers.PrimaryKeyRelatedField(
        queryset=Категория.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'role',
            'full_name',
            'phone',
            'address',
            'city',
            'postal_code',
            'favorite_category',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('пользователь', {})
        if 'email' in user_data:
            instance.пользователь.email = user_data['email']
            instance.пользователь.save()
        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):
    пользователь = serializers.ReadOnlyField(source='пользователь.username')

    class Meta:
        model = Корзина
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ЭлементКорзины
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    товар = ProductSerializer(read_only=True)

    class Meta:
        model = ЭлементЗаказа
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    пользователь = serializers.ReadOnlyField(source='пользователь.username')
    элементы = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Заказ
        fields = [
            'id',
            'пользователь',
            'дата_создания',
            'дата_обновления',
            'адрес_доставки',
            'город',
            'почтовый_индекс',
            'телефон',
            'сумма_заказа',
            'статус',
            'примечание',
            'элементы',
        ]
