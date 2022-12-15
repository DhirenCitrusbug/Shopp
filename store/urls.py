from django.urls import path
from store.views import *

urlpatterns = [
    path('', index,name='index'),
    path('products/', products,name='products'),
    path('search/', search,name='search'),
    path('products/product_detail/<slug>', product_detail,name='product_detail'),
    path('contact/', contact,name='contact'),
    path('login/', login,name='login'),
    path('register/', register,name='register'),
    path('logout/', logout,name='logout'),
    path('checkout/', checkout,name='checkout'),

    # Cart

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/',cart_detail,name='cart_detail'),
]
