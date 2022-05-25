from django.conf.urls import url, include
from django.contrib import admin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', include('users.urls')),
	path('', include('quiz.urls')),
    path('', include('assignment.urls')),
    path('', include('announcements.urls')),
    path('', include('courses.urls')),

    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

