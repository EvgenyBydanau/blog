from django.conf.urls import url
from .autocomplete import CountryAutocomplete

from . import views

urlpatterns = [

    url(r'^create/$', views.post_create, name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.post_detail, name="detail"),
    url(r'^$', views.post_list, name="list"),
    url(r'^(?P<id>[0-9]+)/edit/$', views.post_update, name="update"),
    url(r'^(?P<id>[0-9]+)/delete/$', views.post_delete, name="delete"),
    url(r'^(?P<id>[0-9]+)/comment_add/', views.add_comment_to_post, name="comment_add"),

    # Autocomplete
    url(r'^country-autocomplete/$', CountryAutocomplete.as_view(),  name='country-autocomplete',)

]
