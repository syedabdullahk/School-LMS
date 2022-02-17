from django.shortcuts import redirect, render
from .models import *
from .forms import *


# Create your views here.
def home(request):
    return render(request, 'index.html')


def createQuiz(request):
    form = addQuizform()
    if request.method == 'POST':
        form = addQuizform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/create-question')
    context = {'form': form}
    return render(request, 'addquiz.html', context)


def createQuestions(request):
    form = addQuestionform()
    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'addquestion.html', context)


'''
def qpage(request):
    questions = QuesModel.objects.all()
    dict: questions
    if (request.method == 'POST'):
        print(request.POST.dict())
    return render(request, 'quiz.html', {'questions': questions})'''


def quizzes(request):
    quizzes = QuizModel.objects.all()

    return render(request, 'quizzes.html', {'quizzes': quizzes})


def results(request):
    quizzes = QuizModel.objects.all()

    return render(request, 'Results.html', {'quizzes': quizzes})



def generateresult(id):

    answers = AnswerModel.objects.filter(Question_ID__Quiz_ID=id)
    quiz_id = QuizModel.objects.get(Quiz_ID=id)
    correct = 0
    incorrect = 0

    for i in answers:
        if i.isCorrect:
            correct += 1
        else:
            incorrect += 1


    res = ResultModel(Quiz_ID=quiz_id, Marks=correct)
    res.save()

def attemptquiz(request, id):
    questions = QuesModel.objects.filter(Quiz_ID=id)
    # dict = request.POST.dict()
    if request.method == 'POST':
        dict = request.POST.dict()
        dict.pop('csrfmiddlewaretoken')
        # print(dict.items())

        for k, v in dict.items():
            q_id = QuesModel.objects.get(id=k)
            is_correct = q_id.answer == v
            print(is_correct)

            ans = AnswerModel(Question_ID=q_id, Answer=v, isCorrect=is_correct)
            ans.save()

        answers = AnswerModel.objects.all()

        generateresult(id)

        return render(request, 'answers.html', {'answers': answers})

    return render(request, 'quiz.html', {'questions': questions})


def result(request, id):
    quiz_id = QuizModel.objects.get(Quiz_ID=id)
    results = ResultModel.objects.filter(Quiz_ID=quiz_id)

    if results.exists():
        print('yes', results)

        return render(request, 'result.html', {'results': results})

    else:
        message = 'You havent attempted this quiz yet'
        return render(request, 'result.html', {'message': message})

    return render(request, 'result.html', {'results': results})
