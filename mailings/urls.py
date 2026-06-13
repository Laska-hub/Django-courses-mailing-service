from django.urls import path
from .views import run_mailing

app_name = 'mailings'

urlpatterns = [
    path('<int:pk>/run/', run_mailing, name='run'),
]

