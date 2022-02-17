from django.shortcuts import render


def questions(request):
	return render(request, 'quiz.html')

def login(request):
	return render(request, 'username.html')

