from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from accounts.models import User
from .forms import LoginForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from django.views import generic
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView

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

    