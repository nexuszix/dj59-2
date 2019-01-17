from django.conf.urls import url
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.summary_list, name='main'),
    path('<int:pk>', views.summary_list, name='main_with_param'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^api/$', views.summary_by_date_api, name='summary'),
    path('api/<int:pk>', views.summary_by_date_api, name='summary_with_param'),
]

urlpatterns = format_suffix_patterns(urlpatterns)