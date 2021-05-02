from django.db import models
from django.contrib.auth import get_user_model

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