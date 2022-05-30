from django.conf.urls import url
from django.urls import path, include


from . import views
app_name = "announcements"
urlpatterns = [

	path("create", views.CreateAnnouncementView.as_view(), name="create"),
	path("course", views.AnnouncementListView.as_view(), name='announcement-list'),
	path("", views.AllAnnouncements.as_view(), name='all-announcements'),
	path("detail/<int:pk>", views.AnnouncementDetail.as_view(), name='announcement-detail'),
	path("delete/<int:pk>", views.DeleteAnnouncement.as_view(), name='delete'),

	 
 # _____________ Courses URLs__________________#
    url(r'^api/announcement$', views.Announcement_list),
    url(r'^api/announcement/(?P<pk>[0-9]+)$', views.Announcement_detail),
    url(r'^api/announcement/published$', views.Announcement_list_active),



]
