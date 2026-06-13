from django.urls import path
from .views import (
    RecipientListView,
    RecipientCreateView,
    RecipientDetailView,
    RecipientUpdateView,
    RecipientDeleteView
)

app_name = 'clients'

urlpatterns = [
    path('', RecipientListView.as_view(), name='list'),
    path('create/', RecipientCreateView.as_view(), name='create'),
    path('<int:pk>/', RecipientDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', RecipientUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', RecipientDeleteView.as_view(), name='delete'),
]
