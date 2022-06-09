

from django.views import generic

from courses.models import Course, Enrollment
from assignment.models import Assignment
# Create your views here.


#importing serializer requirements
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404 ,redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from courses .serializers import CourseSerializer
from courses .serializers import EnrollmentSerializer
from courses .models import Course
from courses .models import Enrollment

class CourseDetail(generic.DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

    def get_context_data(self,**kwargs):
        assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['assignments'] = assignments
        self.request.session['course'] = self.kwargs['pk']
        return context
    #saves the id of the selected course to the request.session so it can be used to select relevant assigments/quizzes/announcements
def select_course(request,pk):
    request.session['course'] = pk
    return redirect('/')


class CourseListView(generic.ListView):

    model = Course
   # courses = Course.objects.filter()
   
   
#________________For Courses____________________#
@api_view(['GET', 'POST', 'DELETE'])
def course_list(request):
    if request.method == 'GET':
        tutorials = Course.objects.all()
        
        title = request.query_params.get('course_name', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = CourseSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = CourseSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Course.objects.all().delete()
        return JsonResponse({'message': '{} Courses were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    try: 
        tutorial = Course.objects.get(pk=pk) 
    except Course.DoesNotExist: 
        return JsonResponse({'message': 'The Course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = CourseSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = CourseSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def course_list_active(request):
    tutorials = Course.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = CourseSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#Course part ended here
    
#________________Enrollment____________________#

@api_view(['GET', 'POST', 'DELETE'])
def enrollment_list(request):
    if request.method == 'GET':
        tutorials = Enrollment.objects.all()
        
        title = request.query_params.get('course', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = EnrollmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = EnrollmentSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Enrollment.objects.all().delete()
        return JsonResponse({'message': '{} Enrollment were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def enrollment_detail(request, pk):
    try: 
        tutorial = Enrollment.objects.get(pk=pk) 
    except Enrollment.DoesNotExist: 
        return JsonResponse({'message': 'The Enrollment does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = EnrollmentSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = EnrollmentSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Enrollment was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def Enrollment_list_active(request):
    tutorials = Enrollment.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = EnrollmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#Enrollment part ended here
    