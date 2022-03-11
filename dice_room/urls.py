from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views as views

urlpatterns = [
    path('', views.index),
    path('', include('room.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
]
handler404 = RedirectView.as_view(url='/')
