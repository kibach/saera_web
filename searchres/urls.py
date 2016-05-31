from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^results/?$', views.search_result),
    url(r'^index/?$', views.indexing_url),
    url(r'^view/?$', views.editing_url),
    url(r'^status/?$', views.status),
    url(r'^about/?$', views.about),
    url(r'^status/delete/([0-9]+)/?$', views.url_delete),
    url(r'^status/html/([0-9]+)/?$', views.url_html),
    url(r'^status/plain/([0-9]+)/?$', views.url_plain),
]