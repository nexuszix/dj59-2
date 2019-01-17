from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.summary_list, name='main'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^summary/$', views.summary_by_date_api, name='summary'),
]

urlpatterns = format_suffix_patterns(urlpatterns)