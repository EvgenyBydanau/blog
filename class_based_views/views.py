from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import (
   CreateView,
   DetailView,
   ListView,
   UpdateView,
   DeleteView
)

from posts.models import Post
from .forms import PostModelForm
from .mixins import ListMixin

# Create your views here.


class BaseView(ListMixin, View):
    def get(self, request, *args, **kwargs):
        object_list = super(BaseView, self).get_posts_list()
        return render(request, 'class-based-views/post_list.html', locals())


class PostListView(ListView):
    template_name = 'class-based-views/post_list.html'
    queryset = Post.objects.all() # <class-based_views>/<modelname>_list.html
    paginate_by = 10


class PostDetailView(DetailView):
    template_name = 'class-based-views/post_detail.html'
    queryset = Post.objects.all() # <class-based_views>/<modelname>_list.html

    def get_object(self,  queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)


class PostCreateView(CreateView):
    template_name = 'class-based-views/post_create.html'
    form_class = PostModelForm
    queryset = Post.objects.all() # <class-based_views>/<modelname>_list.html
    success_url = ""

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        return "/class-based-views/post/{}".format(pk)


class PostUpdateView(UpdateView):
    template_name = 'class-based-views/post_create.html'
    form_class = PostModelForm
    success_url = ""

    def get_object(self,  queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        return "/class-based-views/post/{}".format(pk)


class PostDeleteView(DeleteView):
    template_name = 'class-based-views/post_delete.html'

    def get_object(self,  queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)

    def get_success_url(self):
        return reverse('class-based-views:post-list')



