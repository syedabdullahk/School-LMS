from django.conf.urls import url
from django.urls import path, include


from . import views
app_name = "announcements"
urlpatterns = [

	path("announcements/create", views.CreateAnnouncementView.as_view(), name="create"),
	path("announcements/list", views.AnnouncementListView.as_view(), name='announcement-list'),
	path("announcements/detail/<int:pk>", views.AnnouncementDetail.as_view(), name='detail'),
	path("announcements/delete/<int:pk>", views.DeleteAnnouncement.as_view(), name='delete'),




]
