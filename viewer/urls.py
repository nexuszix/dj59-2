from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.render_list, name='main'),
    url(r'^upload/$', views.upload, name='upload'),
]