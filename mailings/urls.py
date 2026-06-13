from django.urls import path
from .views import RunMailingView

app_name = 'mailings'

urlpatterns = [
    path('<int:pk>/run/', RunMailingView.as_view(), name='run'),
]



