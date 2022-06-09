from django.conf.urls import url
from django.urls import path, include


from . import views
app_name = "courses"
urlpatterns = [


	path("course-list", views.CourseListView.as_view(), name='course-list'),
	path("detail/<int:pk>", views.CourseDetail.as_view(), name='course-detail'),
    path("select/<int:pk>", views.select_course, name='course-select'),
 
     # _____________ Courses URLs__________________#
    url(r'^api/courses$', views.course_list),
    url(r'^api/courses/(?P<pk>[0-9]+)$', views.course_detail),
    url(r'^api/courses/published$', views.course_list_active),
    
    # _____________ Enrollment URLs__________________#
    url(r'^api/enrollment$', views.enrollment_list),
    url(r'^api/enrollment/(?P<pk>[0-9]+)$', views.enrollment_detail),
    url(r'^api/enrollment/published$', views.Enrollment_list_active),
]
