from django.conf.urls import url
from . import views
app_name='travels'
urlpatterns = [
    url(r'^$', views.show, name='show'),
    url(r'^add$', views.add, name='add'),
    url(r'^add/create$', views.create, name='create'),
    url(r'^join/(?P<trip_id>\d+)$', views.join, name='join'),
    url(r'^destination/(?P<t_id>\d+)$', views.destination, name='destination'),
    # # url(r'^add$', views.new, name='add'),
    # # url(r'^create$', views.create, name='create')
]
