from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register_view, verify_email


urlpatterns = [
    # =========================
    # регистрация
    # =========================
    path(
        "register/",
        register_view,
        name="register"
    ),

    # =========================
    # логин
    # =========================
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="auth/login.html"
        ),
        name="login"
    ),

    # =========================
    # logout
    # =========================
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # =========================
    # подтверждение email
    # =========================
    path(
        "verify/<uuid:token>/",
        verify_email,
        name="verify_email"
    ),

    # =========================
    # восстановление пароля
    # =========================
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset.html"
        ),
        name="password_reset"
    ),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
