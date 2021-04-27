from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from accounts.models import User
from .forms import LoginForm, SignUpForm, UserChangeForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from django.views import generic
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




User = get_user_model()

# Create your views here.
class LoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

class SignupView(FormView, CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # アクティベーションURLの送付
            current_site = get_current_site(self.request)
            domain = current_site.domain
            context = {
                'protocol': self.request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }

            subject = render_to_string('accounts/mail_template/signup/subject.txt', context)
            message = render_to_string('accounts/mail_template/signup/message.txt', context)

            user.email_user(subject, message)
            return redirect('accounts:accounts_signup_done')

class SignupDoneView(TemplateView):
    template_name = 'accounts/signup_done.html'


class SignupCompleteView(TemplateView):
    template_name = 'accounts/signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()




class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuse

class UserDeleteView(OnlyYouMixin, DeleteView):
    template_name = "accounts/delete_user.html"
    success_url = reverse_lazy("index")
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('index')
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'username' : self.request.user.username,
            'email' : self.request.user.email,
            'state' : self.request.user.state,
            'city' : self.request.user.city,
            'zipcode' : self.request.user.zipcode,
            'phone_number' : self.request.user.phone_number,
        })
        return kwargs


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = User
    template_name = 'accounts/password_change.html'
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    slug_field = 'username'
    slug_url_kwarg = 'username'


class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordReset(PasswordResetView):
    # """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/password_reset/subject.txt'
    email_template_name = 'accounts/mail_template/password_reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    # """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    # """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    # """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'
