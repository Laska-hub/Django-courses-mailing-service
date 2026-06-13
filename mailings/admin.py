from django.contrib import admin
from .models import Mailing, Attempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        for obj in qs:
            obj.update_status()
        return qs


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'mailing',
        'status',
        'attempt_time',
        'server_response'
    )

    list_filter = ('status', 'attempt_time')



