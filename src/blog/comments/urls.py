from django.conf.urls import url

from .views import (
    comment_thread,
    comment_delete,
)

urlpatterns = [
    # url(r'^$', views.post_list, name="home"),
    # url(r'^create/$', views.post_create, name='create'),
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete),
    ]
