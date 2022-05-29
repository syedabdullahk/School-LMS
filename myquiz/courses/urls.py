from django.conf.urls import url
from django.urls import path, include


from . import views
app_name = "courses"
urlpatterns = [


	path("course-list", views.CourseListView.as_view(), name='course-list'),
	path("detail/<int:pk>", views.CourseDetail.as_view(), name='course-detail'),
]
