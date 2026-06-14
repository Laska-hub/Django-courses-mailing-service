from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings',
        null=True,
        blank=True
    )

    message = models.ForeignKey(
        'messages_app.Message',
        on_delete=models.CASCADE,
        related_name='mailings'
    )

    recipients = models.ManyToManyField(
        'clients.Recipient',
        related_name='mailings'
    )

    # =========================
    # 🔥 ВАЛИДАЦИЯ (КЛЮЧЕВОЕ ДЛЯ ЗАЩИТЫ)
    # =========================
    def clean(self):
        now = timezone.now()

        if self.start_time and self.end_time:

            # ❗ start не может быть в прошлом
            if self.start_time < now:
                raise ValidationError(
                    {"start_time": "Start time не может быть в прошлом"}
                )

            # ❗ логическая проверка интервала
            if self.start_time >= self.end_time:
                raise ValidationError(
                    {"end_time": "End time должен быть позже start time"}
                )

    # =========================
    # SAVE (чтобы clean работал везде)
    # =========================
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # =========================
    # ДИНАМИЧЕСКИЙ СТАТУС
    # =========================
    def update_status(self):
        now = timezone.now()

        if not self.start_time or not self.end_time:
            return

        if now < self.start_time:
            new_status = 'created'
        elif self.start_time <= now <= self.end_time:
            new_status = 'started'
        else:
            new_status = 'finished'

        if self.status != new_status:
            self.status = new_status

            # ⚠️ важно: НЕ вызываем save() с full_clean логикой
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Mailing #{self.id} - {self.status}"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    server_response = models.TextField(
        blank=True,
        null=True
    )

    attempt_time = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Attempt {self.status} ({self.attempt_time:%Y-%m-%d %H:%M})"
