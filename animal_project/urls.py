
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve 

from . import settings_mysql_local
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("adopt_animals.urls")),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),

    path('oauth/', include('social_django.urls', namespace='social')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] 

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings_mysql_local.MEDIA_URL, document_root=settings_mysql_local.MEDIA_ROOT)
