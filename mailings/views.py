from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from clients.models import Recipient
from mailings.models import Mailing, Attempt
from mailings.services import send_mailing


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['total_recipients'] = Recipient.objects.count()

        # ✔ ДОБАВИЛИ СТАТИСТИКУ ATTEMPTS
        context['attempts_success'] = Attempt.objects.filter(status='success').count()
        context['attempts_failed'] = Attempt.objects.filter(status='failed').count()

        return context


# ✔ CBV запуск рассылки (ВАЖНО ПО ТЗ)
class RunMailingView(View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        result = send_mailing(mailing)
        return HttpResponse(result)
