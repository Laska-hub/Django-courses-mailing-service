from django.contrib import admin
from .models import Mailing, Attempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'status',
        'start_time',
        'end_time',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        for obj in qs:
            obj.update_status()

        if request.user.is_superuser or getattr(request.user, 'is_manager', False):
            return qs

        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user

        super().save_model(request, obj, form, change)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'mailing',
        'status',
        'attempt_time',
        'server_response',
    )

    list_filter = (
        'status',
        'attempt_time',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or getattr(request.user, 'is_manager', False):
            return qs

        return qs.filter(mailing__owner=request.user)

