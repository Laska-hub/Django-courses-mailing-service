from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Recipient
from .forms import RecipientForm


class RecipientListView(ListView):
    model = Recipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'clients/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('clients:list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('clients:list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'clients/recipient_confirm_delete.html'
    success_url = reverse_lazy('clients:list')

