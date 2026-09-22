from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.cache import cache

from clients.models import Recipient
from messages_app.models import Message

from .models import Mailing, Attempt
from .services import send_mailing
from .forms import MailingForm


# =========================
# HOME PAGE (STATISTICS + CACHE)
# =========================
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "/users/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = "home_stats"
        stats = cache.get(cache_key)

        if stats is None:
            mailings = Mailing.objects.all()

            stats = {
                "total_mailings": mailings.count(),
                "active_mailings": mailings.filter(status="started").count(),
                "total_recipients": Recipient.objects.count(),
                "attempts_success": Attempt.objects.filter(status="success").count(),
                "attempts_failed": Attempt.objects.filter(status="failed").count(),
            }

            cache.set(cache_key, stats, 60)

        context.update(stats)
        return context


# =========================
# MAILING LIST
# =========================
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"
    login_url = "/users/login/"

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name="Manager").exists():
            return Mailing.objects.all()

        return Mailing.objects.filter(owner=user)


# =========================
# MAILING DETAIL
# =========================
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self):
        obj = super().get_object()
        obj.update_status()
        return obj


# =========================
# MAILING CREATE
# =========================
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        cache.delete("home_stats")
        return response


# =========================
# MAILING UPDATE
# =========================
class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


# =========================
# MAILING DELETE
# =========================
class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


# =========================
# RUN MAILING (BUSINESS LOGIC)
# =========================
class RunMailingView(LoginRequiredMixin, View):

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if not (
            request.user.is_superuser
            or request.user.groups.filter(name="Manager").exists()
        ):
            return HttpResponse("Нет доступа", status=403)

        result = send_mailing(mailing)

        cache.delete("home_stats")
        cache.delete(f"mailings_list_{request.user.id}")

        return HttpResponse(result)
