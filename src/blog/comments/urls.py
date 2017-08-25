from django.conf.urls import url

from .views import (
    comment_thread,

)

urlpatterns = [
    # url(r'^$', views.post_list, name="home"),
    # url(r'^create/$', views.post_create, name='create'),
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
    ]
