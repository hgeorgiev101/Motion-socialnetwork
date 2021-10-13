from django.urls import path

from registration_profile.views import CreateRegistrationView, ValidateCreateRegistrationView

urlpatterns = [
    path('', CreateRegistrationView.as_view()),
    path('validation/', ValidateCreateRegistrationView.as_view()),
]
