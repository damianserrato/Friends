from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^logout$', views.logout),
    url(r'^view/(?P<id>\d+)$', views.view),
    url(r'^remove/(?P<id>\d+)$', views.remove),
]