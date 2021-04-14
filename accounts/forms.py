from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import (User, State, get_user_model)
from django import forms
from phone_field import PhoneField
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

class SignUpForm(UserCreationForm, forms.ModelForm):

    state = forms.ModelChoiceField(
                          queryset=State.objects.all(),
                          widget=forms.Select, label="State:", required=True)

    city = forms.CharField(
                          label="City:", required=True)

    zipcode = forms.CharField(
                          label="Zip Code:", required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'state', 'city', 'zipcode', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email