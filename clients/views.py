from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Recipient
from .forms import RecipientForm


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, 'is_manager', False):
            return Recipient.objects.all()

        return Recipient.objects.filter(owner=user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'clients/recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, 'is_manager', False):
            return Recipient.objects.all()

        return Recipient.objects.filter(owner=user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'clients/recipient_form.html'
    success_url = '/clients/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
