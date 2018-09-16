#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    information_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # post = models.ForeignKey(Post)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentManager()

    def __str__(self):
        return str(self.user.email)


class Country(models.Model):
    text = models.CharField(verbose_name='Country', max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Creation date", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Update date", auto_now=True)

    def __str__(self):
        return self.text


class UserPhone(models.Model):
    user = models.ForeignKey('accounts.User')
    code = models.CharField(verbose_name="Code", max_length=10, blank=True, null=True)
    number = models.CharField(verbose_name="Number", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Creation date", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Update date", auto_now=True)

    def __str__(self):
        return str(self.number)


