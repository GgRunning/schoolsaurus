from django.conf.urls import url
from django.contrib.auth import views as auth_controller
from sso import controllers

app_name = 'sso'
urlpatterns = [
    url(r'^login/$',
        controllers.LoginView.as_view(template_name='sso/login/index.html'),
        name='login'),
    url(r'^alogin/$',
	controllers.alogin,
        name='alogin'),
    url(r'^register/$',
        controllers.register,
        name='register'),
    url(r'^aregister/$',
        controllers.aregister,
        name='aregister'),
    url(r'^logout/$', auth_controller.logout, {'next_page': '/'}, name='logout'),
    url(r'^verify/(?P<token>\w+)/$',
        controllers.verify,
        name='verify'),
]
