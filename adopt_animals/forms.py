from django import forms
from .models import Post, Tag, Message
from accounts.models import User, get_user_model
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# 下記で写真にサイズ制限をかける
def file_size(value): 
  limit = 2 * 1024 * 1024
  if value.size > limit:
      raise ValidationError('File too large. Size should not exceed 2 MB.')

class PostForm(forms.ModelForm):

  title = forms.CharField(label='Title', required=True)
  name = forms.CharField(label='Name', required=True)
  age = forms.IntegerField(label='Age', required=True)
  photo = forms.ImageField(label='Image', validators=[file_size])
  photo2 = forms.ImageField(label='Image2', required=False, validators=[file_size])
  photo3 = forms.ImageField(label='Image3', required=False, validators=[file_size])
  photo4 = forms.ImageField(label='Image4', required=False, validators=[file_size])
  photo5 = forms.ImageField(label='Image5', required=False, validators=[file_size])
  sex = forms.fields.ChoiceField(
      choices = (
          ('1', 'Male'),
          ('2', 'Female'),
          ), 
         required=True,
         widget=forms.widgets.Select
         )
  weight = forms.IntegerField(label='Weight', required=False)
  story = forms.CharField(label='Story', required=True)
#   下記のempty_label=Noneはプルダウンメニューをクリックすると--------という項目を非表示にできる
  category = forms.ModelChoiceField(queryset=Tag.objects.all(),
                      widget=forms.Select, label="Category:", required=True, empty_label=None)
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