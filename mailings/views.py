from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.cache import cache

from clients.models import Recipient
from .models import Mailing, Attempt
from .services import send_mailing


# =========================
# HOME PAGE (СТАТИСТИКА + CACHE)
# =========================
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = "home_stats"
        stats = cache.get(cache_key)

        if stats is None:

            mailings = Mailing.objects.all()

            # 🔥 динамическое обновление статуса (ТЗ)
            for m in mailings:
                m.update_status()

            stats = {
                "total_mailings": mailings.count(),

                "active_mailings": mailings.filter(
                    status='started'
                ).count(),

                "total_recipients": Recipient.objects.count(),

                "attempts_success": Attempt.objects.filter(
                    status='success'
                ).count(),

                "attempts_failed": Attempt.objects.filter(
                    status='failed'
                ).count(),
            }

            cache.set(cache_key, stats, 60)

        context.update(stats)
        return context


# =========================
# MAILING LIST (РОЛИ + CACHE)
# =========================
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'
    login_url = '/users/login/'

    def get_queryset(self):
        user = self.request.user

        cache_key = f"mailings_list_{user.id}"
        cached = cache.get(cache_key)

        if cached is not None:
            return cached

        # 🔥 роли (ТЗ)
        if user.is_superuser or getattr(user, 'is_manager', False):
            qs = Mailing.objects.all()
        else:
            qs = Mailing.objects.filter(owner=user)

        # важно: сразу список (чтобы кеш не ломался)
        qs = list(qs)

        cache.set(cache_key, qs, 30)
        return qs


# =========================
# RUN MAILING (БИЗНЕС-ЛОГИКА + ЗАЩИТА)
# =========================
class RunMailingView(LoginRequiredMixin, View):

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # 🔥 защита доступа
        if not (
            request.user.is_superuser
            or getattr(request.user, 'is_manager', False)
        ):
            return HttpResponse("Нет доступа", status=403)

        # 🔥 запуск рассылки (batch Attempt внутри services)
        result = send_mailing(mailing)

        # 🔥 сброс кеша после изменения данных
        cache.delete("home_stats")
        cache.delete(f"mailings_list_{request.user.id}")

        return HttpResponse(result)
