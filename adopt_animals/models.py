from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Tag(models.Model):
  category = models.CharField(verbose_name='Animal Category', max_length=20, null=False, blank=False)

class Post(models.Model):
  title = models.TextField(verbose_name='State', max_length=300, null=False, blank=False)
  name = models.CharField(verbose_name='Name', max_length=40, null=False, blank=False)
  age = models.IntegerField(verbose_name='Age', null=False, blank=False)
  photo = models.ImageField(upload_to='images', verbose_name='Photo', null=False, blank=False)
  sex = models.IntegerField(verbose_name='Sex', null=False, blank=False)
  weight = models.IntegerField(verbose_name='Weight', null=False, blank=False)
  story = models.TextField(verbose_name='Story', max_length=300, null=False, blank=False)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='user')
  category = models.ForeignKey(Tag, verbose_name='Category', on_delete=models.CASCADE)