from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wishlist$', views.wishlist),
    url(r'^logout$', views.logout),
    url(r'^wishlist/create$', views.create),
    url(r'^wishlist/create/add', views.add),
    url(r'^wishlist/(?P<id>\d+)$', views.item),
    url(r'^remove/(?P<id>\d+)$', views.remove),
]