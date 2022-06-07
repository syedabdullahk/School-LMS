from django.db import models
from courses.models import Course
from django.urls import reverse
from users.models import User


class QuizModel(models.Model):
    Quiz_ID = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    Quiz_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Quiz_name

    def get_absolute_url(self):
        return reverse('quiz:create-question',kwargs={'pk':self.pk})


class QuesModel(models.Model):
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=20)
    option2 = models.CharField(max_length=20)
    option3 = models.CharField(max_length=20)
    option4 = models.CharField(max_length=20)
    answer = models.CharField(max_length=20)
    Quiz_ID = models.ForeignKey(QuizModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class AnswerModel(models.Model):
    Answer_ID = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, related_name="answer", on_delete=models.CASCADE)
    Answer = models.CharField(max_length=200, null=True)
    Question_ID = models.ForeignKey(QuesModel, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(default = True)

class ResultModel(models.Model):
    student = models.ForeignKey(User, related_name="result", on_delete=models.CASCADE)
    Quiz_ID = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    Marks = models.IntegerField()