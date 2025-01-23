from django.urls import path
from . import views

urlpatterns = [
    path('', views.minha_view, name='home'),
]
