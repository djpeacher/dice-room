from django.urls import path
from . import views as views

urlpatterns = [
    path('chat/', views.Chat.as_view()),
    path('name/', views.Name.as_view()),
    path('dice/', views.Dice.as_view()),
    path('dice/<str:formula>/', views.Dice.as_view()),
    path('z/', views.Zone.as_view()),
    path('z/<str:zone_name>/', views.Zone.as_view()),
]
