from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Review, CartItem, ContactMessage
from .forms import UserRegistrationForm, UserLoginForm, ReviewForm, ContactForm


def index(request):
    """Главная страница"""
    # Безопасное получение отзывов (если таблица еще не создана)
    try:
        reviews = Review.objects.all()[:10]  # Последние 10 отзывов
    except Exception as e:
        # Если таблица еще не создана, используем пустой список
        reviews = []
    
    if request.method == 'POST' and 'review' in request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('index')
    else:
        form = ReviewForm()
    
    context = {
        'reviews': reviews,
        'review_form': form,
    }
    return render(request, 'index.html', context)


def catalog(request):
    """Каталог товаров"""
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    return render(request, 'katalog.html', context)


def contacts(request):
    """Страница контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'kontakts.html', context)


def about(request):
    """Страница о нас"""
    return render(request, 'about.html')


def privacy(request):
    """Страница политики конфиденциальности"""
    return render(request, 'privacy.html')


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def user_login(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Использует сессии (куки)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            
            # Редирект на следующую страницу или профиль
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


@login_required
def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('index')


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_cart_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'user': user,
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
    }
    return render(request, 'profile.html', context)


@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} добавлен в корзину.')
    return redirect('catalog')


@login_required
def remove_from_cart(request, cart_item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} удален из корзины.')
    return redirect('profile')


@login_required
def update_cart_item(request, cart_item_id):
    """Обновление количества товара в корзине"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Корзина обновлена.')
    else:
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины.')
    
    return redirect('profile')

