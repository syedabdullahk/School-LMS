from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth.mixins import (LoginRequiredMixin)

# ___________________ Serializar ______________#
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from announcements .models import Announcement
from announcements .serializers import AnnouncementSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


def about(request):
    return render(request, 'about.html', {})
def indexdocs(request):
    return render(request, 'indexdocs.html', {})
class CreateAnnouncementView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAnnouncementForm
    template_name = 'announcements/createannouncement_form.html'

    # success_url = reverse('assignments:submit_detail')
    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.author = self.request.user
        obj.course = self.request.session.get('course')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateAnnouncementView, self).get_context_data(**kwargs)

        context['time'] = timezone.now()
        return context

class AllAnnouncements(generic.ListView):

    # All Announcements that concern the logged in student
    model = Announcement
    template_name = 'index.html'


    def get_context_data(self):

        context = super(AllAnnouncements, self).get_context_data()

        if self.request.user.user_type == 1:
            announcements = Announcement.objects.filter(course__in = Course.objects.filter(students=self.request.user))

        else:
            announcements = Announcement.objects.filter(course__in=Course.objects.filter(teacher=self.request.user))

        context['object_list'] = announcements
        return context

class AnnouncementListView(generic.ListView):
    model = Announcement

    def get_context_data(self):

        context = super(AnnouncementListView, self).get_context_data()

        if  self.request.user.user_type ==2:
            context['object_list'] = self.request.user.announcement.all()
        else:
            #show only announcements of the selected Course
            filtered_announcements = Announcement.objects.filter(course__id=self.request.session.get('course'))
            context['object_list'] = filtered_announcements

        return context


class AnnouncementDetail(LoginRequiredMixin, generic.DetailView):
    model = Announcement

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetail, self).get_context_data(**kwargs)
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        context['announcement'] = announcement
        return context

class DeleteAnnouncement(LoginRequiredMixin, generic.DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcements:announcement-list')
    
    
    
    
    # ________________________ Serializer Announcement ____________________--#
    
@api_view(['GET', 'POST', 'DELETE'])
def Announcement_list(request):
    if request.method == 'GET':
        tutorials = Announcement.objects.all()
        
        title = request.query_params.get('subject', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = AnnouncementSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = AnnouncementSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Announcement.objects.all().delete()
        return JsonResponse({'message': '{} Announcement were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def Announcement_detail(request, pk):
    try: 
        tutorial = Announcement.objects.get(pk=pk) 
    except Announcement.DoesNotExist: 
        return JsonResponse({'message': 'The Announcement does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = AnnouncementSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = AnnouncementSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Announcement was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def Announcement_list_active(request):
    tutorials = Announcement.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = AnnouncementSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
