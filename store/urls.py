from django.urls import path
from store.views import index

urlpatterns = [
    path('', index,name='index'),
]