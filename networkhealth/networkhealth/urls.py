"""networkservices URL Configuration

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
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^switchcommands.html$', views.switchcommand, name='switchcommand'),
    url(r'^routercommands.html$', views.routercommand, name='routercommand'),
    url(r'^health.html$', views.health, name='health'),
    url(r'^switchcommand/$', views.switchcommand, name='switchcommand'),
    url(r'^firewall.html$', views.firewalls, name='firewalls'),
    url(r'^asa.html$', views.asa, name='asa'),
    url(r'^alloutstations.html$', views.all_sites, name='allsites'),
]
