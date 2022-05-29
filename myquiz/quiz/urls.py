from django.conf.urls import url
from django.urls import path, include

import quiz.views as quiz_views
from . import views
app_name = "quiz"
urlpatterns = [


	path("", views.home, name="home"),
	#path("questions/", views.qpage, name="questions"),


	path("add-quiz", views.CreateQuizView.as_view(), name="create-quiz"),


	path("create-question/<int:pk>", views.createQuestions, name="create-question"),
	#path("quizzes", views.quizzes, name="quizzes"),
	#temporary
	path("quizzes/<int:pk>", views.QuizListView.as_view(), name="quizzes"),
	#temporary
	path("results", views.results, name="results"),
	path("answers", views.attemptquiz, name="answers"),
	path("attempt-quiz/<int:id>", views.attemptquiz, name="attempt-quiz"),
	path("results/<int:id>", views.result, name="quiz-result"),

	path('htmx/create-quiz-form', views.create_quiz_form, name='create-quiz-form'),
	path("testadd", views.test_add_quiz, name="testadd"),


]
