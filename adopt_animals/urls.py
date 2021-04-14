from django.urls import path
from .views import IndexView
from adopt_animals import views
from accounts import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

]