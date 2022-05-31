from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.urls import path, include
from users import views


app_name = 'users'

urlpatterns = [
path('accounts/login/', auth_views.LoginView.as_view(template_name="users/login.html"), name = "login"),
path('accounts/logout/', auth_views.LogoutView.as_view(),name = "logout"),

    # _____________ Users URLs__________________#
url(r'^api/users$', views.user_list),
url(r'^api/users/(?P<pk>[0-9]+)$', views.user_detail),
url(r'^api/users/published$', views.user_list_active),


]