from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Attempt


class MailingServiceError(Exception):
    """Базовая ошибка сервиса рассылок."""
    pass


class MailingTimeError(MailingServiceError):
    """Ошибка времени рассылки."""
    pass


def send_mailing(mailing):
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        raise MailingTimeError(
            "Рассылка может выполняться только в заданном временном интервале"
        )

    attempts = []
    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )

            attempts.append(
                Attempt(
                    mailing=mailing,
                    status="success",
                    server_response="OK",
                )
            )

        except Exception as error:
            attempts.append(
                Attempt(
                    mailing=mailing,
                    status="failed",
                    server_response=str(error),
                )
            )

    Attempt.objects.bulk_create(attempts)

    return {
        "mailing_id": mailing.id,
        "total_attempts": len(attempts),
        "success": len([a for a in attempts if a.status == "success"]),
        "failed": len([a for a in attempts if a.status == "failed"]),
    }
