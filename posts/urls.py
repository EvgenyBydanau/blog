from django.conf.urls import url
from .autocomplete import CountryAutocomplete

from . import views

urlpatterns = [

    url(r'^create/$', views.post_create, name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.post_detail, name="detail"),
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', views.post_list, name="list-filtered"),
    url(r'^$', views.post_list, name="list"),
    url(r'^(?P<id>[0-9]+)/edit/$', views.post_update, name="update"),
    url(r'^(?P<id>[0-9]+)/delete/$', views.post_delete, name="delete"),
    url(r'get-weather$', views.get_weather, name="get-weather"),
    url(r'read-xml$', views.read_xml, name="read-xml"),
    url(r'aggregate-countries$', views.aggregate_countries, name='aggregate_countries'),
    url(r'annotate$', views.annotate, name='annotate'),
    url(r'get-country/(?P<id>[0-9]+)/$', views.get_country, name='get_country'),

    # Autocomplete
    url(r'^country-autocomplete/$', CountryAutocomplete.as_view(),  name='country-autocomplete',)

]
