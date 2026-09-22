from django.urls import path

from .views import (
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    RunMailingView,
)

app_name = "mailings"

urlpatterns = [
    path("", MailingListView.as_view(), name="list"),
    path("create/", MailingCreateView.as_view(), name="create"),
    path("<int:pk>/", MailingDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="delete"),
    path("<int:pk>/run/", RunMailingView.as_view(), name="run"),
]
