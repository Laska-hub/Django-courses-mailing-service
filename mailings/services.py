from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Attempt


def send_mailing(mailing):
    now = timezone.now()

    # =========================
    # ❗ 1. Проверка временного окна
    # =========================
    if not (mailing.start_time <= now <= mailing.end_time):
        return "Ошибка: рассылка вне допустимого времени"

    # =========================
    # ❗ 2. Получатели
    # =========================
    recipients = mailing.recipients.all()

    if not recipients.exists():
        return "Ошибка: нет получателей для рассылки"

    # =========================
    # ❗ 3. Подготовка message (безопасно)
    # =========================
    subject = getattr(mailing.message, "subject", "")
    body = getattr(mailing.message, "body", "")

    attempts = []

    # =========================
    # ❗ 4. Отправка писем
    # =========================
    for recipient in recipients:
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )

            attempts.append(
                Attempt(
                    mailing=mailing,
                    status="success",
                    server_response="OK"
                )
            )

        except Exception as e:
            attempts.append(
                Attempt(
                    mailing=mailing,
                    status="failed",
                    server_response=str(e)
                )
            )

    # =========================
    # ❗ 5. BATCH CREATE (КРИТЕРИЙ ТЗ)
    # =========================
    Attempt.objects.bulk_create(attempts)

    return f"Отправка завершена. Попыток: {len(attempts)}"
