from django.contrib import admin
from django.urls import path, include
from mailings.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✔ ГЛАВНАЯ СТРАНИЦА
    path('', HomeView.as_view(), name='home'),

    # ✔ MAILINGS
    path('mailings/', include('mailings.urls')),
]



