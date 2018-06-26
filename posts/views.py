from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from collections import Counter
import datetime
from .models import Post
from .forms import PostForm, CommentForm
from .decorators import superuser_only_user_post_author


def post_list(request, date=None):
    if date:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        posts_list = Post.objects.filter(timestamp__month=date.month,
                                         timestamp__year=date.year).order_by("-timestamp")
    else:
        posts_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts_list, 5)
    '''
     Convert datetime object to str '2018-06-01'
     then convert this str to  datetime object '2018-06-01'
     then make list with tuples [(date(year, month, 1), number of posts)]
     which is number of posts for specific year-month
     '''
    year_month = []
    posts_timestamps = Post.objects.values_list('timestamp', flat=True).order_by('-timestamp')
    for date in posts_timestamps:
        new_date = date.strftime('%Y-%m')
        new_date_object = datetime.datetime.strptime(new_date, "%Y-%m").date()
        year_month.append(new_date_object)
    unique_year_month = list(Counter(year_month).items())

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "post_list.html", locals())


@login_required(login_url='/login/')
@superuser_only_user_post_author
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "The post was successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "post_form.html", locals())


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    return render(request, "post_detail.html", locals())


@login_required(login_url='/login/')
@superuser_only_user_post_author
def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The post was successfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "post_form.html", locals())


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








