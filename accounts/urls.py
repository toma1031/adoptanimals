from django.urls import path
from accounts import views
from accounts.views import (LoginView, SignupView, SignupDoneView, SignupCompleteView, UserDeleteView, UserChangeView)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('signup/', SignupView.as_view(), name='accounts_signup'),
    path('signup/done/', SignupDoneView.as_view(), name='accounts_signup_done'),
    path('signup/complete/<token>/', SignupCompleteView.as_view(), name='accounts_signup_complete'),

    path('<str:username>/delete/', UserDeleteView.as_view(), name='accounts_delete_user'),

    path('<str:username>/change/', UserChangeView.as_view(), name="accounts_change_user"),
]