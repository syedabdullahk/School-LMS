from django.conf.urls import url, include
from django.contrib import admin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path("about", views.about, name="about"),
    path("indexdocs", views.indexdocs, name="indexdocs"),

    path('', include('users.urls')),
	path('', include('quiz.urls')),
    path('', include('assignment.urls')),
    path('announcements/', include('announcements.urls')),
    path('courses/', include('courses.urls')),
    path('about.html', include('courses.urls')),
    path('indexdocs.html', include('courses.urls')),
    
    
    path('api-auth/', include('rest_framework.urls')),

    path('admin', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

