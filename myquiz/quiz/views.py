from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views import generic
# Serializers import
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from quiz .models import QuesModel
from quiz .models import QuizModel
from quiz .models import ResultModel
from quiz .models import AnswerModel
from quiz .serializers import QuesModelSerializer
from quiz .serializers import QuizModelSerializer
from quiz .serializers import ResultModelSerializer
from quiz .serializers import AnswerModelSerializer
from courses .models import Course



# Create your views here.
def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}

    return render(request, 'index.html',context)


class CreateQuizView(LoginRequiredMixin, generic.CreateView):

    model  = QuizModel
    form_class = addQuizform
    template_name = 'addquiz.html'
    select_related = ('course')


    # success_url = reverse('assignments:submit_detail')
    def form_valid(self, form):
        obj = form.save(commit=False)
        course = Course.objects.get(pk=self.request.session.get('course'))
        obj.course= course
        self.request.session['quiz'] = obj.Quiz_ID
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(CreateQuizView, self).get_context_data(**kwargs)
        return context

@user_passes_test(lambda user: user.user_type == 2)
def test_add_quiz(request,pk):
    form = addQuestionform()
    request.session['quiz'] = pk


    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.Quiz_ID_id = request.session['quiz']
            form.save()
            return HttpResponse('success')
        else:
            return render(request, "quiz/partials/quiz_form.html", context={
                "form": form
            })
    context = {'form': form}
    return render(request, 'quiz/create_questions.html', context)

@user_passes_test(lambda user: user.user_type == 2)
def create_quiz_form(request):
    form = addQuestionform()
    quiz = QuizModel.objects.get(Quiz_ID=request.session['quiz'])
    context = {
        "form": form,
        "quiz":quiz
    }
    return render(request, "quiz/partials/quiz_form.html", context)




@user_passes_test(lambda user: user.user_type == 2)
def createQuestions(request,pk):

    quiz = QuizModel.objects.get(Quiz_ID=pk)
    form = addQuestionform()

    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.Quiz_ID_id =pk
            form.save()
            return HttpResponse("success")
    context = {'form': form}
    return render(request, 'addquestion.html', context)





def quizzes(request,id):
    request.session['course'] = id
    quizzes = QuizModel.objects.filter(course = id)

    return render(request, 'quizzes.html', {'quizzes': quizzes})

class QuizListView(generic.ListView):
    model = QuizModel
    template_name = 'quizzes.html'

    def get_context_data(self, **kwargs):


        context = super(QuizListView, self).get_context_data(**kwargs)

        quizzes = QuizModel.objects.filter(course=self.kwargs['pk'])
        context['object_list'] = quizzes
        self.request.session['course'] = self.kwargs['pk']
        return context


def results(request):
    quizzes = QuizModel.objects.all()

    return render(request, 'Results.html', {'quizzes': quizzes})



def generateresult(id,student_id):

    answers = AnswerModel.objects.filter(Question_ID__Quiz_ID=id ,student = student_id)
    quiz_id = QuizModel.objects.get(Quiz_ID=id)
    correct = 0
    incorrect = 0

    for i in answers:
        if i.isCorrect:
            correct += 1
        else:
            incorrect += 1


    res = ResultModel(Quiz_ID=quiz_id, Marks=correct, student = student_id)
    res.save()

def attemptquiz(request, id):
    questions = QuesModel.objects.filter(Quiz_ID=id)
    student_id = request.user
    if request.method == 'POST':
        dict = request.POST.dict()
        dict.pop('csrfmiddlewaretoken')
        # print(dict.items())

        for k, v in dict.items():
            q_id = QuesModel.objects.get(id=k)
            is_correct = q_id.answer == v
            ans = AnswerModel(Question_ID=q_id, Answer=v, isCorrect=is_correct, student = student_id)
            ans.save()

        answers = AnswerModel.objects.all()



        generateresult(id,student_id)

        return redirect('/')

    return render(request, 'quiz.html', {'questions': questions})


def result(request, id):
    quiz_id = QuizModel.objects.get(Quiz_ID=id)
    results = ResultModel.objects.filter(Quiz_ID=quiz_id, student = request.user )

    if results.exists():

        return render(request, 'result.html', {'results': results})

    else:
        message = 'You havent attempted this quiz yet'
        return render(request, 'result.html', {'message': message})

    return render(request, 'result.html', {'results': results})

# __________________ Serializer View setting ____________________#

# ___________________________________________________________________________________________________________________


#________________For Quiz Model ____________________#

@api_view(['GET', 'POST', 'DELETE'])
def QuizModel_list(request):
    if request.method == 'GET':
        tutorials = QuizModel.objects.all()
        
        title = request.query_params.get('Quiz_name', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = QuizModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = QuizModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = QuizModel.objects.all().delete()
        return JsonResponse({'message': '{} QuizModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def QuizModel_detail(request, pk):
    try: 
        tutorial = QuizModel.objects.get(pk=pk) 
    except QuizModel.DoesNotExist: 
        return JsonResponse({'message': 'The QuizModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = QuizModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = QuizModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'QuizModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def QuizModel_list_active(request):
    tutorials = QuizModel.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = QuizModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#QuizModel part ended here
    
    #________________For QuesModel____________________#

@api_view(['GET', 'POST', 'DELETE'])
def QuesModel_list(request):
    if request.method == 'GET':
        tutorials = QuesModel.objects.all()
        
        title = request.query_params.get('Quiz_ID', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = QuesModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = QuesModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = QuesModel.objects.all().delete()
        return JsonResponse({'message': '{} QuesModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def QuesModel_detail(request, pk):
    try: 
        tutorial = QuesModel.objects.get(pk=pk) 
    except QuesModel.DoesNotExist: 
        return JsonResponse({'message': 'The QuesModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = QuesModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = QuesModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'QuesModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def QuesModel_list_active(request):
    tutorials = QuesModel.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = QuesModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#QuesModel part ended here
    
    #________________For ResultModel ____________________#

@api_view(['GET', 'POST', 'DELETE'])
def ResultModel_list(request):
    if request.method == 'GET':
        tutorials = ResultModel.objects.all()
        
        title = request.query_params.get('Quiz_ID', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = ResultModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = ResultModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = ResultModel.objects.all().delete()
        return JsonResponse({'message': '{} ResultModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def ResultModel_detail(request, pk):
    try: 
        tutorial = ResultModel.objects.get(pk=pk) 
    except ResultModel.DoesNotExist: 
        return JsonResponse({'message': 'The ResultModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = ResultModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = ResultModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'ResultModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def ResultModel_list_active(request):
    tutorials = ResultModel.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = ResultModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#ResultModel part ended here
    
    #________________For Answer____________________#

@api_view(['GET', 'POST', 'DELETE'])
def AnswerModel_list(request):
    if request.method == 'GET':
        tutorials = AnswerModel.objects.all()
        
        title = request.query_params.get('Answer_ID', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = AnswerModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = AnswerModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = AnswerModel.objects.all().delete()
        return JsonResponse({'message': '{} AnswerModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def AnswerModel_detail(request, pk):
    try: 
        tutorial = AnswerModel.objects.get(pk=pk) 
    except AnswerModel.DoesNotExist: 
        return JsonResponse({'message': 'The AnswerModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = AnswerModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = AnswerModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'AnswerModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
# @api_view(['GET'])
# def AnswerModel_list_active(request):
#     tutorials = AnswerModel.objects.filter(published=True)
        
#     if request.method == 'GET': 
#         tutorials_serializer = AnswerModelSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#AnswerModel part ended here
    
    
