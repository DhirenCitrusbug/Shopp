from django.urls import path
from store.views import *

urlpatterns = [
    path('', index,name='index'),
    path('products/', products,name='products'),
    path('search/', search,name='search'),
]