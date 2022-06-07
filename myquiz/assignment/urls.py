from django.conf.urls import url
from django.urls import path, include


from . import views
app_name = "assignment"
urlpatterns = [

	path("create", views.CreateAssignment2.as_view(), name="create"),
	path("submit", views.SubmitAssignmentView.as_view(), name="submit"),
	path("assignment-list/<int:pk>", views.AssignmentListView.as_view(), name='assgn-list'),
	path("detail/<int:pk>", views.AssignmentDetail.as_view(), name='detail'),
	#path("submit-detail/<int:pk>", views.AssignmentDetail.as_view(), name='submit-detail'),
	path("submission-detail/<int:pk>", views.SubmitAssignmentDetail.as_view(), name='submit_detail'),
 
     # _____________ Assignment URLs__________________#
    url(r'^api/assignment$', views.assignment_list),
    url(r'^api/assignment/(?P<pk>[0-9]+)$', views.assignment_detail),
    url(r'^api/assignment/published$', views.assignment_list_active),
    
    # _____________ SubmitAssignment URLs__________________#
    url(r'^api/submitassignment$', views.submitAssignment_list),
    url(r'^api/submitassignment/(?P<pk>[0-9]+)$', views.submitAssignment_detail),
    url(r'^api/submitassignment/published$', views.submitAssignment_list_active),



]
