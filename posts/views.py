from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import Http404

import json

from .models import Post
from .forms import PostForm, CommentForm


@login_required(login_url='/login/')
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "The post was successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request, "There was an error")

    context = {
        "form": form
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    # print(request.session.keys())
    # print(request.session['_auth_user_id'])

    posts_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
       posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
       posts = paginator.page(paginator.num_pages)
    context = {
       "posts": posts
    }
    return render(request, "post_list.html", context)



def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The post was successfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context={
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "The post was deleted")
    return redirect("posts:list")


@login_required(login_url='/login/')
def add_comment_to_post(request, id):
    title = "Add comment"
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts:detail', id=id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, "title": title})








