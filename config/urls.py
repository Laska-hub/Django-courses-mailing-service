from django.contrib import admin
from django.urls import path, include

from mailings.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница
    path('', HomeView.as_view(), name='home'),

    # Рассылки
    path('mailings/', include('mailings.urls')),

    # Получатели
    path('clients/', include('clients.urls')),

    # Сообщения
    path('messages/', include('messages_app.urls')),

    # Пользователи
    path('users/', include('users.urls')),
]
