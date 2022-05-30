from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os
from django.conf import settings

# from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

#importing serializer requirements
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from assignment .models import Assignment
from assignment .models import SubmitAssignment
from assignment .serializers import AssignmentSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from assignment .serializers import SubmitAssignmentSerializer

# Create your views here.



class CreateAssignment2(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignment/createAssignment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SubmitAssignmentView(LoginRequiredMixin, generic.CreateView):
    form_class = SubmitAssignmentForm
    template_name = 'assignment/submitassignment_form.html'
    select_related = ('author', 'assignment_ques')

    # success_url = reverse('assignments:submit_detail')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        assignments = Assignment.objects.get(pk=self.request.session.get('assignment'))
        obj.assignment_ques = assignments
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        assignments = Assignment.objects.filter(pk=self.request.session.get('assignment'))
        assignment_object = get_object_or_404(assignments)
        context = super(SubmitAssignmentView, self).get_context_data(**kwargs)
        context['duedate'] = assignment_object.due_date
        context['time'] = timezone.now()
        return context



class SubmitAssignmentDetail(LoginRequiredMixin, generic.DetailView):
    model = SubmitAssignment
    template_name = 'assignment/assignment_submissions.html'

    def get_context_data(self, **kwargs):
        submissions = SubmitAssignment.objects.filter(pk=self.kwargs['pk'])
        submissions_object = get_object_or_404(submissions)
        context = super(SubmitAssignmentDetail, self).get_context_data(**kwargs)
        context['submissions'] = submissions_object
        return context


class AssignmentDetail(LoginRequiredMixin, generic.DetailView,generic.FormView):
    model = Assignment
    form_class = SubmitAssignmentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        assignments = Assignment.objects.get(pk=self.request.session.get('assignment'))
        obj.assignment_ques = assignments
        obj.submitted_date = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # course_obj = Course.objects.filter(students=self.request.user.id)
        context = super(AssignmentDetail, self).get_context_data(**kwargs)
        # context['course'] = course_obj
        assignment = Assignment.objects.filter(pk=self.kwargs['pk'])
        assignment_object = get_object_or_404(assignment)
        context['duedate'] = assignment_object.due_date
        context['time'] = timezone.now()
        submitassignment = SubmitAssignment.objects.filter(assignment_ques=self.kwargs['pk'])
        context['submitted'] = submitassignment
        self.request.session['assignment'] = self.kwargs['pk']
        # print(self.request.session['assignment'])
        return context


class AssignmentListView(generic.ListView):
    model = Assignment

    def get_context_data(self, **kwargs):

        context = super(AssignmentListView, self).get_context_data(**kwargs)
        filtered_assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        context['object_list'] = filtered_assignments
        return context

    # the default template is (lowercase)<modelname>_list
class AssignmentSubmitDetail(LoginRequiredMixin, generic.DetailView,generic.FormView):

    model = SubmitAssignment



@api_view(['GET', 'POST', 'DELETE'])
def assignment_list(request):
    if request.method == 'GET':
        tutorials = Assignment.objects.all()
        
        title = request.query_params.get('assignment_name', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = AssignmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = AssignmentSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Assignment.objects.all().delete()
        return JsonResponse({'message': '{} Assignments were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def assignment_detail(request, pk):
    try: 
        tutorial = Assignment.objects.get(pk=pk) 
    except Assignment.DoesNotExist: 
        return JsonResponse({'message': 'The Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = AssignmentSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = AssignmentSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Assignment was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def assignment_list_active(request):
    tutorials = Assignment.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = AssignmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#Assingent part ended here
    
#________________ Submit Assignment ____________________#

@api_view(['GET', 'POST', 'DELETE'])
def submitAssignment_list(request):
    if request.method == 'GET':
        tutorials = SubmitAssignment.objects.all()
        
        title = request.query_params.get('author', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = SubmitAssignmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = SubmitAssignmentSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Assignment.objects.all().delete()
        return JsonResponse({'message': '{} Submitted Assignment were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def submitAssignment_detail(request, pk):
    try: 
        tutorial = SubmitAssignment.objects.get(pk=pk) 
    except SubmitAssignment.DoesNotExist: 
        return JsonResponse({'message': 'The Submitted Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = AssignmentSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = SubmitAssignmentSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Assignment was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def submitAssignment_list_active(request):
    tutorials = SubmitAssignment.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = SubmitAssignmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#Enrollment part ended here

    
