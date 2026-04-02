from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Товар, Категория, Производитель, Корзина, ЭлементКорзины
from django.contrib.auth.models import User


# ==================== Страницы из предыдущего задания ====================

def home(request):
    """Главная страница с ссылками на другие страницы"""
    return render(request, 'shop/home.html')


def about_author(request):
    """Страница об авторе"""
    return render(request, 'shop/about.html')


def store_info(request):
    """Страница о магазине настольных игр"""
    return render(request, 'shop/store.html')


# ==================== Задание 2: Представления для каталога и корзины ====================

def product_list(request):
    """
    Список товаров с фильтрацией по категории, производителю
    и поиском по названию и описанию
    """
    товары = Товар.objects.select_related('категория', 'производитель').all()
    
    # Получаем параметры фильтрации из GET-запроса
    категория_id = request.GET.get('category')
    производитель_id = request.GET.get('manufacturer')
    поиск = request.GET.get('search')
    
    # Фильтрация по категории
    if категория_id:
        товары = товары.filter(категория_id=категория_id)
    
    # Фильтрация по производителю
    if производитель_id:
        товары = товары.filter(производитель_id=производитель_id)
    
    # Поиск по названию и описанию (используем Q-объекты)
    if поиск:
        товары = товары.filter(
            Q(название__icontains=поиск) | Q(описание__icontains=поиск)
        )
    
    # Получаем списки категорий и производителей для фильтров
    категории = Категория.objects.all()
    производители = Производитель.objects.all()
    
    context = {
        'товары': товары,
        'категории': категории,
        'производители': производители,
        'selected_category': категория_id,
        'selected_manufacturer': производитель_id,
        'search_query': поиск,
    }
    
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """
    Детальная информация о товаре по его ID
    """
    товар = get_object_or_404(
        Товар.objects.select_related('категория', 'производитель'),
        pk=pk
    )
    
    context = {
        'товар': товар,
    }
    
    return render(request, 'shop/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    """
    Добавление товара в корзину
    Доступно только аутентифицированным пользователям
    """
    товар = get_object_or_404(Товар, pk=product_id)
    
    # Получаем или создаём корзину пользователя
    корзина, _ = Корзина.objects.get_or_create(пользователь=request.user)
    
    # Получаем количество из POST-запроса (по умолчанию 1)
    количество = int(request.POST.get('quantity', 1))
    
    # Проверяем, есть ли уже такой товар в корзине
    элемент, created = ЭлементКорзины.objects.get_or_create(
        корзина=корзина,
        товар=товар,
        defaults={'количество': количество}
    )
    
    if not created:
        # Если товар уже есть, увеличиваем количество
        элемент.количество += количество
        элемент.save()
    
    # Проверяем валидацию
    if элемент.количество > товар.количество_на_складе:
        messages.error(
            request,
            f'Недостаточно товара на складе. Доступно: {товар.количество_на_складе}'
        )
        элемент.количество = min(элемент.количество, товар.количество_на_складе)
        элемент.save()
    else:
        messages.success(request, f'Товар "{товар.название}" добавлен в корзину')
    
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    """
    Обновление количества товара в корзине
    """
    элемент = get_object_or_404(ЭлементКорзины, pk=item_id)
    
    # Проверяем, что корзина принадлежит текущему пользователю
    if элемент.корзина.пользователь != request.user:
        messages.error(request, 'Вы не можете редактировать эту корзину')
        return redirect('cart')
    
    if request.method == 'POST':
        количество = int(request.POST.get('quantity', 1))
        
        # Валидация: количество не должно превышать наличие на складе
        if количество > элемент.товар.количество_на_складе:
            messages.error(
                request,
                f'Недостаточно товара на складе. Доступно: {элемент.товар.количество_на_складе}'
            )
            количество = элемент.товар.количество_на_складе
        
        if количество <= 0:
            # Если количество 0 или меньше, удаляем элемент
            элемент.delete()
            messages.info(request, 'Товар удалён из корзины')
        else:
            элемент.количество = количество
            элемент.save()
            messages.success(request, 'Количество товара обновлено')
    
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    """
    Удаление товара из корзины
    """
    элемент = get_object_or_404(ЭлементКорзины, pk=item_id)
    
    # Проверяем, что корзина принадлежит текущему пользователю
    if элемент.корзина.пользователь != request.user:
        messages.error(request, 'Вы не можете редактировать эту корзину')
        return redirect('cart')
    
    название_товара = элемент.товар.название
    элемент.delete()
    messages.success(request, f'Товар "{название_товара}" удалён из корзины')
    
    return redirect('cart')


@login_required
def cart_view(request):
    """
    Просмотр корзины пользователя
    """
    # Получаем корзину пользователя или создаём новую
    корзина, created = Корзина.objects.get_or_create(
        пользователь=request.user
    )
    
    # Получаем все элементы корзины
    элементы = корзина.элементы.select_related('товар').all()
    
    # Вычисляем общую стоимость
    общая_стоимость = корзина.общая_стоимость()
    
    context = {
        'корзина': корзина,
        'элементы': элементы,
        'общая_стоимость': общая_стоимость,
    }
    
    return render(request, 'shop/cart.html', context)
