from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Категория


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    full_name = forms.CharField(required=False, label='ФИО')
    phone = forms.CharField(required=False, label='Телефон')
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label='Адрес доставки')
    city = forms.CharField(required=False, label='Город')
    postal_code = forms.CharField(required=False, label='Почтовый индекс')
    favorite_category = forms.ModelChoiceField(
        queryset=Категория.objects.all(),
        required=False,
        label='Любимая категория'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'phone', 'address', 'city', 'postal_code', 'favorite_category')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
