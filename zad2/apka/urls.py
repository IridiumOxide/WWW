from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<gmina_numer>[0-9]*)/$', views.gmina_menu, name='gmina_menu'),
    url(r'^obwod/(?P<obwod_numer>[0-9]*)/$', views.obwod, name='obwod'),
]