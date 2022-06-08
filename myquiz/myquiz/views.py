from django.shortcuts import render


def questions(request):
	return render(request, 'quiz.html')

def login(request):
	return render(request, 'username.html')
def about(request):
	return render(request, 'about.html')
def indexdocs(request):
	return render(request, 'indexdocs.html')

