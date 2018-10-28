from django.conf.urls import url


from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
app_name = 'class-based-views'
urlpatterns = [

    url(r'^post-list/$', PostListView.as_view(), name="post-list"),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name="post-detail"),
    url(r'^create/$', PostCreateView.as_view(), name="post-create"),
    url(r'^update/(?P<pk>[0-9]+)/$', PostUpdateView.as_view(), name="post-update"),
    url(r'^delete/(?P<pk>[0-9]+)/$', PostDeleteView.as_view(), name="post-delete"),

]
