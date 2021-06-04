from django.contrib import admin
from .models import Message, MessageRoom, Post, Tag, Like


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Message)
admin.site.register(MessageRoom)
