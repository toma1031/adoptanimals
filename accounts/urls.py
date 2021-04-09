from django.urls import path
from accounts import views
from accounts.views import (LoginView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='accounts_login'),
]