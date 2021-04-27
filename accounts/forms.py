from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .models import (User, State, get_user_model)
from django import forms
from phone_field import PhoneField
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

class SignUpForm(UserCreationForm, ModelForm):

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


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'state',
            'city',
            'zipcode',
            'phone_number',
            
        ]

    def __init__(self, username=None, email=None, state=None, city=None,  zipcode=None, phone_number=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if username:
            self.fields['username'].widget.attrs['value'] = username
        if email:
            self.fields['email'].widget.attrs['value'] = email
        if state:
            self.fields['state'].widget.attrs['value'] = state
        if city:
            self.fields['city'].widget.attrs['value'] = city
        if zipcode:
            self.fields['zipcode'].widget.attrs['value'] = zipcode
        if phone_number:
            self.fields['phone_number'].widget.attrs['value'] = phone_number
        



    def update(self, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.state = self.cleaned_data['state']
        user.city = self.cleaned_data['city']
        user.zipcode = self.cleaned_data['zipcode']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()

class MyPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = [
            'password1', 
            'password2',
        ]

class MyPasswordResetForm(PasswordResetForm):
    # """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    # """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'