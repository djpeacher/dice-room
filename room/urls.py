from django.urls import path
from . import views as views

urlpatterns = [
    path('join/', views.join),
    path('<str:room_name>/', views.room),
]
