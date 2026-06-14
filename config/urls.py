from django.contrib import admin
from django.urls import path, include
from mailings.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),

    path('mailings/', include('mailings.urls')),

    path('users/', include('users.urls')),
]




