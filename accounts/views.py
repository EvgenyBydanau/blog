from django.shortcuts import render,redirect
from django.contrib.auth import (
   authenticate,
   get_user_model,
   login,
   logout
)
from accounts.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.http import HttpResponseRedirect
from django import forms
from django.http import Http404
from django.contrib import messages

# Create your views here.


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "login_form.html", {"form": form, "title": title})


def register_view(request):
    title = "Register"
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            # user = form.save(commit=False)
            if not (User.objects.filter(email=form.cleaned_data['email']).exists()):
                User.objects.create_user(email=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'],
                                         country=form.cleaned_data['country'],
                                         birth_date=form.cleaned_data['birth_date'])
                # user.set_password(user.password)
                # user.save()
                user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data.get('password'))
                login(request, user)
                return HttpResponseRedirect('/')
            else:
               raise forms.ValidationError('Userrrr with that email or password already exists')
    return render(request, "registration_form.html", locals())


def logout_view(request):
    logout(request)
    return redirect("/")



def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()
    messages.success(request, "Your account is verified")
    return redirect('/')



