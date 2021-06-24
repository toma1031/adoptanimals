from django import forms
from .models import Post, Tag, Message
from accounts.models import User, get_user_model
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

# 下記で写真にサイズ制限をかける
def file_size(value): 
  limit = 2 * 1024 * 1024
  if value.size > limit:
      raise ValidationError('File too large. Size should not exceed 2 MB.')

class PostForm(forms.ModelForm):

  title = forms.CharField(
        label='Title', 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Title",
        }),
    )
  name = forms.CharField(
        label='Name', 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "name",
        }),
    )
  age = forms.IntegerField(
        label='Age', 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Age",
        }),
    )

# widget=forms.FileInputとすることでCurrentryとChangeを一旦全て削除
# 参考箇所（https://stackoverflow.com/questions/14336925/how-to-not-render-django-image-field-currently-and-clear-stuff）
  photo = forms.ImageField(label='Image', validators=[file_size], widget=forms.FileInput)
  photo2 = forms.ImageField(label='Image2', required=False, validators=[file_size], widget=forms.FileInput)
  photo3 = forms.ImageField(label='Image3', required=False, validators=[file_size], widget=forms.FileInput)
  photo4 = forms.ImageField(label='Image4', required=False, validators=[file_size], widget=forms.FileInput)
  photo5 = forms.ImageField(label='Image5', required=False, validators=[file_size], widget=forms.FileInput)
  sex = forms.fields.ChoiceField(
      choices = (
          ('1', 'Male'),
          ('2', 'Female'),
          ), 
         required=True,
         widget=forms.widgets.Select(attrs={
                'class': 'form-control',
            }),
         )
  weight = forms.IntegerField(
        label='Weight', 
        required=False,
        widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Weight",
        }),
    )
  story = forms.CharField(
        label='Story', 
        required=True,
        widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Story",
        }),
    )
#   下記のempty_label=Noneはプルダウンメニューをクリックすると--------という項目を非表示にできる
  category = forms.ModelChoiceField(queryset=Tag.objects.all(),
        label="Category:", required=True, empty_label=None, 
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
# このMetaの中身というのはmodelsのフィールドを元にしている
  class Meta:
      model = Post
      fields = [
          'title',
          'name',
          'age',
          'photo',
          'photo2',
          'photo3',
          'photo4',
          'photo5',
          'sex',
          'weight',
          'story',
          'category',
      ]


class MessageForm(forms.ModelForm):
  message = forms.CharField(label='message', required=True)

# このMetaの中身というのはmodelsのフィールドを元にしている
  class Meta:
      model = Message
      fields = [
          'message',
      ]

# お問い合わせフォーム
class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Name",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Email",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Message",
        }),
    )

    def send_email(self):
        subject = "Inquery"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("An invalid header has been detected.")
