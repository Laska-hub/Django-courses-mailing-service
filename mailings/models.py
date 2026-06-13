from django.db import models
from django.utils import timezone


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

    message = models.ForeignKey(
        'messages_app.Message',
        on_delete=models.CASCADE,
        related_name='mailings'
    )

    recipients = models.ManyToManyField(
        'clients.Recipient',
        related_name='mailings'
    )

    def update_status(self):
        """
        Обновляет статус рассылки в зависимости от текущего времени
        """
        now = timezone.now()

        if now < self.start_time:
            new_status = 'created'
        elif self.start_time <= now <= self.end_time:
            new_status = 'started'
        else:
            new_status = 'finished'

        if self.status != new_status:
            self.status = new_status
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

    server_response = models.TextField(blank=True, null=True)

    attempt_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt {self.status} ({self.attempt_time:%Y-%m-%d %H:%M})"
