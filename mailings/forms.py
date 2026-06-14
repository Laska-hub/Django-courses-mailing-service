from django import forms
from django.utils import timezone

from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ['owner']

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        now = timezone.now()

        if start_time and start_time < now:
            self.add_error('start_time', 'Нельзя выбрать прошлое время.')

        if start_time and end_time:
            if start_time >= end_time:
                self.add_error('end_time', 'Окончание должно быть позже начала.')

        return cleaned_data
