from .models import Post
from django.contrib import messages
from django.shortcuts import redirect


def superuser_only(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.warning(request, "Only superusers can create or edit posts")
            return redirect("posts:list")
        if 'id' in kwargs:
            post = Post.objects.get(pk=kwargs['id'])
            if post.user == request.user:
                return function(request, *args, **kwargs)
            else:
                messages.warning(request, "You can't edit the post")
                return redirect("posts:list")
        return function(request, *args, **kwargs)
    return wrapper


def user_is_post_author(function):
    def wrapper(request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['id'])
        if post.user == request.user:
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "You can't edit the post")
            return redirect("posts:list")
    return wrapper
