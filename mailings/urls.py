from django.urls import path
from .views import HomeView, RunMailingView, MailingListView

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/run/', RunMailingView.as_view(), name='run'),
]


