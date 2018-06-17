#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

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


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class Country(models.Model):
    text = models.CharField(verbose_name='Country', max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Creation date", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Update date", auto_now=True)

    def __str__(self):
        return self.text


