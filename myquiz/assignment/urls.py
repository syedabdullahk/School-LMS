from django.conf.urls import url
from django.urls import path, include


from . import views
app_name = "assignment"
urlpatterns = [

	path("create", views.CreateAssignment2.as_view(), name="create"),
	path("submit", views.SubmitAssignmentView.as_view(), name="submit"),
	path("assignment-list", views.AssignmentListView.as_view(), name='assgn-list'),
	path("detail/<int:pk>", views.AssignmentDetail.as_view(), name='detail'),
	#path("submit-detail/<int:pk>", views.AssignmentDetail.as_view(), name='submit-detail'),
	path("submission-detail/<int:pk>", views.SubmitAssignmentDetail.as_view(), name='submit_detail'),



]
