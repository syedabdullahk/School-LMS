from django.conf.urls import url, include
from django.contrib import admin

from django.urls import path, include


urlpatterns = [

	path('', include('quiz.urls')),

    url(r'^admin/', admin.site.urls),
]

