from django.contrib import admin
from .models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'owner')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or getattr(request.user, 'is_manager', False):
            return qs

        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user

        super().save_model(request, obj, form, change)
