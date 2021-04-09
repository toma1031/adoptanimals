from django.contrib.auth.forms import AuthenticationForm
from .models import (get_user_model)
from django import forms

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)