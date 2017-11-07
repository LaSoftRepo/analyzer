"""analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import views
from django.shortcuts import render
from rest_framework import routers

# from analyzer.users.views import UserViewSet
from rest_framework.reverse import reverse_lazy
from rest_framework_swagger.views import get_swagger_view

from collection.views import CollectionsViewSet
from parser_olx.views import parse
from settings_analyzer.views import SettingsViewSet, StatusViewSet, \
    StopWordViewSet
from users.views import UserViewSet

schema_view = get_swagger_view(title='Parser API')

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'users/current_user', UserViewSet, base_name='current_user')
router.register(r'users/get_email', UserViewSet, base_name='get_email')
router.register(r'collections', CollectionsViewSet, base_name='collections')
router.register(r'settings', SettingsViewSet, base_name='settings')
router.register(r'status', StatusViewSet, base_name='status')
router.register(r'stopword', StopWordViewSet, base_name='status')

v1_0_patterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
]
v1_0_patterns += router.urls

@login_required
def index(request):
    # print(reverse_lazy('users'))
    return render(request, 'index.html', {})

urlpatterns = [
    url(r'^$', index),
    url(r'^parse$', parse),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^api/v1.0/', include(v1_0_patterns, namespace='v1.0')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^swagger$', schema_view)

]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', views.serve),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
