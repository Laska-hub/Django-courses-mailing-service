from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from .forms import UserRegisterForm
from .models import User


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False
            user.save()

            verify_link = (
                f"http://127.0.0.1:8001/users/verify/{user.verification_token}/"
            )

            send_mail(
                subject="Подтверждение регистрации",
                message=f"Перейдите по ссылке для подтверждения:\n{verify_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, "auth/check_email.html")

    else:
        form = UserRegisterForm()

    return render(request, "auth/register.html", {"form": form})


def verify_email(request, token):
    user = get_object_or_404(User, verification_token=token)

    user.is_verified = True
    user.save()

    return render(request, "auth/email_verified.html")
