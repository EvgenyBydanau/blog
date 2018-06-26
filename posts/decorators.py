from .models import Post
from django.contrib import messages
from django.shortcuts import redirect


def superuser_only_user_post_author(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.warning(request, "Only superusers can create or edit posts")
            return redirect("posts:list")
        if 'id' in kwargs:
            post = Post.objects.get(pk=kwargs['id'])
            if not post.user == request.user:
                messages.warning(request, "You can't edit the post")
                return redirect("posts:list")
        return function(request, *args, **kwargs)
    return wrapper

