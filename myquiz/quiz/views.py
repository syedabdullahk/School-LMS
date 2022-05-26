from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views import generic


# Create your views here.
def home(request):

    return render(request, 'index.html')

@user_passes_test(lambda user: user.user_type == 2)
def createQuiz(request):
    form = addQuizform()
    obj = form.save(commit=False)
    obj.course = Course.objects.get(pk=request.session.get('course'))
    if request.method == 'POST':
        form = addQuizform(request.POST)
        if form.is_valid():

            form.save()
            return redirect('/create-question')
    context = {'form': form}
    return render(request, 'addquiz.html', context)

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
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(CreateQuizView, self).get_context_data(**kwargs)
        return context








@user_passes_test(lambda user: user.user_type == 2)
def createQuestions(request):
    form = addQuestionform()
    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
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
