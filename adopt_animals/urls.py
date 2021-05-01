from django.urls import path
from .views import IndexView
from adopt_animals import views
from accounts import views
from adopt_animals.views import CreatePostView, PostDoneView

app_name = 'adopt_animals'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('post/new/', CreatePostView.as_view(), name='post_new'), 
    path('post/done/', PostDoneView.as_view(), name='post_done'),
]