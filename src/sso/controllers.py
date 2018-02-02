from django.shortcuts import render
from sso.models import User
from sso.forms import UserCreationForm
from sso.utils import send_email
import random
import string
from django.contrib.auth.views import LoginView as AuthLoginView


class LoginView(AuthLoginView):
    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return '/admin'
        return super(LoginView, self).get_redirect_url()


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
            content = 'Hi, {} <br><br> Thank you for registering for SchoolPedia, ' \
                      'Please confirm your email address by clicking the link below. ' \
                      '<br> <h2><a href=\'http://schoolpedia.herokuapp.com/sso/verify/{}/\'>Validate Account</a></h2>'

            send_email(
                user.email,
                'SchoolPedia Registration',
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
