from django.shortcuts import render
from sso.models import User
from sso.forms import UserCreationForm
from sso.utils import send_email
import random
import string
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
import json

class LoginView(AuthLoginView):
    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return '/admin'
        return super(LoginView, self).get_redirect_url()

def alogin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse('/admin')
            else:
                return HttpResponse(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse("fail")
    else:
        return HttpResponse(json.dumps({"nothing to see"}), content_type="application/json")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            while True:
                custom_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                try:
                    User.objects.get(custom_token=custom_token)
                except User.DoesNotExist:
                    break
            user.custom_token = custom_token
            user.save()

            full_name = user.get_full_name()
            content = 'Hi, {} <br><br> Thank you for registering for Schoolsaurus, ' \
                      'Please confirm your email address by clicking the link below. ' \
                      '<br> <h2><a href=\'http://schoolsaurus.herokuapp.com/sso/verify/{}/\'>Validate Account</a></h2>'

            send_email(
                user.email,
                'Schoolsaurus Registration',
                content.format(full_name, user.custom_token))
            return render(
                request,
                'sso/register/register_success.html',
                {'email': user.email},
            )
        else:
            return render(request, 'sso/register/index.html', {'form': form})
    else:
        Registerform = UserCreationForm()
    return render(request, 'sso/register/index.html', {'Registerform': Registerform})

def aregister(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            while True:
                custom_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                try:
                    User.objects.get(custom_token=custom_token)
                except User.DoesNotExist:
                    break
            user.custom_token = custom_token
            user.save()

            full_name = user.get_full_name()
            content = 'Hi, {} <br><br> Thank you for registering for Schoolsaurus' \
                      'Please confirm your email address by clicking the link below. ' \
                      '<br> <h2><a href=\'http://schoolsaurus.herokuapp.com/sso/verify/{}/\'>Validate Account</a></h2>'

            send_email(
                user.email,
                'Schoolsaurus Registration',
                content.format(full_name, user.custom_token))
            return HttpResponse("success")
        else:
            return HttpResponse(form.errors.as_text())

def verify(request, token):
    try:
        user = User.objects.get(custom_token=token)
    except User.DoesNotExist:
        return render(
            request,
            'sso/register/invalid_token.html',
        )
    if user.is_active is False:
        user.is_active = True
        user.save()
        return render(
            request,
            'sso/register/success_validate_email.html',
        )
    else:
        return render(
            request,
            'sso/register/username_already_validated.html',
        )
