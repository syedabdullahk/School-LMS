from django.conf.urls import url, include
from django.contrib import admin

from django.urls import path, include


urlpatterns = [

    path('', include('users.urls')),
	path('', include('quiz.urls')),
    path('', include('assignment.urls')),
    path('', include('announcements.urls')),

    url(r'^admin/', admin.site.urls),
]

