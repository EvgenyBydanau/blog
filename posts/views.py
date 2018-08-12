from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from collections import Counter
import datetime
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .decorators import superuser_only, user_is_post_author
from django.contrib.contenttypes.models import ContentType


def post_list(request, date=None):
    if date:
        if 'q' in request.GET:
            query = request.GET.get('q')
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            posts_list = Post.objects.filter(Q(timestamp__month=date.month), Q(timestamp__year=date.year),
                                             Q(title__icontains=query) | Q(content__contains=query)).order_by('-timestamp')
            '''Look for q in comments'''
            posts_with_comments = Post.objects.filter(Q(timestamp__month=date.month), Q(timestamp__year=date.year),
                                                        comment__content__icontains=query).order_by('-timestamp')
            '''Exclude multiple posts'''
            posts_list = set(list(chain(posts_list, posts_with_comments)))
            posts_list = sorted(posts_list, key=lambda x: x.timestamp, reverse=True)
        else:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            posts_list = Post.objects.filter(timestamp__month=date.month,
                                             timestamp__year=date.year).order_by("-timestamp")
    else:
        if 'q' in request.GET:
            query = request.GET.get('q')
            posts_list = Post.objects.filter(Q(title__icontains=query) | Q(content__contains=query)).order_by('-timestamp')
            '''Look for q in comments'''
            posts_with_comments = Post.objects.filter(comment__content__icontains=query).order_by('-timestamp')
            '''Exclude multiple posts'''
            posts_list = set(list(chain(posts_list, posts_with_comments)))
            posts_list = sorted(posts_list, key=lambda x: x.timestamp, reverse=True)
        else:
            posts_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts_list, 5)
    '''
     Convert datetime object to str '2018-06-01'
     then convert this str to  datetime object '2018-06-01'
    '''
    year_month = []
    posts_timestamps = Post.objects.values_list('timestamp', flat=True).order_by('-timestamp')
    for date in posts_timestamps:
        new_date = date.strftime('%Y-%m')
        new_date_object = datetime.datetime.strptime(new_date, "%Y-%m").date()
        year_month.append(new_date_object)
    """
    Counter - counts number of post occurrences in year_month list
    then make list with tuples [(date(year, month, 1), number of posts)]
    which is number of posts for specific year-month
    """
    unique_year_month = reversed(sorted(list(Counter(year_month).items())))

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "post_list.html", locals())


@login_required(login_url='/login/')
@superuser_only
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
    comments = instance.comments

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        new_comment, created = Comment.objects.get_or_create(
                                    user=request.user,
                                    content_type=content_type,
                                    object_id=obj_id,
                                    content=content_data
                                   )
        if created:
            print("qwerty")

    return render(request, "post_detail.html", locals())


@login_required(login_url='/login/')
@user_is_post_author
def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The post was successfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "post_form.html", locals())


@user_is_post_author
def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "The post was deleted")
    return redirect("posts:list")






