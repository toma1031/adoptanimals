from django.urls import path
from accounts import views
from accounts.views import (LoginView, SignupView, SignupDoneView, SignupCompleteView)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('signup/', SignupView.as_view(), name='accounts_signup'),
    path('signup/done/', SignupDoneView.as_view(), name='accounts_signup_done'),
    path('signup/complete/<token>/', SignupCompleteView.as_view(), name='accounts_signup_complete'),
]