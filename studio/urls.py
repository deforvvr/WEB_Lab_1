from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('katalog/', views.catalog, name='catalog'),
    path('kontakts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
]

