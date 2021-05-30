from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Tag(models.Model):
  category = models.CharField(verbose_name='Animal Category', max_length=20, null=False, blank=False)

# 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return self.category

class Post(models.Model):
  title = models.CharField(verbose_name='Title', max_length=40, null=False, blank=False)
  name = models.CharField(verbose_name='Name', max_length=40, null=False, blank=False)
  age = models.IntegerField(verbose_name='Age', null=False, blank=False)
  # 写真は５枚アップロードできるようにする
  photo = models.ImageField(upload_to='images/', verbose_name='Photo', null=False, blank=False)
  photo2 = models.ImageField(upload_to='images/', verbose_name='Photo2', null=True, blank=True)
  photo3 = models.ImageField(upload_to='images/', verbose_name='Photo3', null=True, blank=True)
  photo4 = models.ImageField(upload_to='images/', verbose_name='Photo4', null=True, blank=True)
  photo5 = models.ImageField(upload_to='images/', verbose_name='Photo5', null=True, blank=True)
  sex = models.IntegerField(verbose_name='Sex', null=False, blank=False)
  weight = models.IntegerField(verbose_name='Weight', blank=True, null=True)
  story = models.TextField(verbose_name='Story', max_length=300, null=False, blank=False)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='user')
  category = models.ForeignKey(Tag, verbose_name='Category', on_delete=models.CASCADE)

# 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return self.title


class Like(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  timestamp = models.DateTimeField(default=timezone.now)

# 以下を書くことによりcategoryをちゃんとオブジェクト名で表示できる
  def __str__(self):
    return self.post


class MessageRoom(models.Model):
    post = models.ForeignKey(Post, verbose_name='MessageRoom Post', on_delete=models.CASCADE)
    inquiry_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='inquiry_user')

    def __str__(self):
      return str(self.id)
class Message(models.Model):
    message = models.CharField(max_length=100)
    message_room = models.ForeignKey(MessageRoom, verbose_name='Message', on_delete=models.CASCADE)

    def __str__(self):
      return self.message