"""animal_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from . import settings_mysql
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("adopt_animals.urls")),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),

    path('oauth/', include('social_django.urls', namespace='social')),
] 

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings_mysql.MEDIA_URL, document_root=settings_mysql.MEDIA_ROOT)
