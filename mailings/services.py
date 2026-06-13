from django.core.mail import send_mail
from django.utils import timezone

from .models import Mailing, Attempt


def send_mailing(mailing: Mailing):
    now = timezone.now()

    # проверка времени
    if not (mailing.start_time <= now <= mailing.end_time):
        return "Ошибка: рассылка вне допустимого времени"

    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )

            Attempt.objects.create(
                mailing=mailing,
                status='success',
                server_response='OK'
            )

        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                status='failed',
                server_response=str(e)
            )

    mailing.update_status()

    return "Рассылка выполнена"
