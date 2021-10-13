from django.urls import path

from registration_profile.views import CreateRegistrationView, ValidateCreateRegistrationView, PasswordResetView, \
    PasswordResetValidationView

urlpatterns = [
    path('registration/', CreateRegistrationView.as_view()),
    path('registration/validation/', ValidateCreateRegistrationView.as_view()),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset/validation/', PasswordResetValidationView.as_view()),
]
