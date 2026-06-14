from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Message
from .forms import MessageForm


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, 'is_manager', False):
            return Message.objects.all()

        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messages/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, 'is_manager', False):
            return Message.objects.all()

        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('messages:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('messages:list')

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, 'is_manager', False):
            return Message.objects.all()

        return Message.objects.filter(owner=user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages/message_confirm_delete.html'
    success_url = reverse_lazy('messages:list')

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, 'is_manager', False):
            return Message.objects.all()

        return Message.objects.filter(owner=user)
