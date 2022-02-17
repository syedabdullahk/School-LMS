from django.db import models


class QuizModel(models.Model):
    Quiz_ID = models.AutoField(primary_key=True)
    Course_ID = models.CharField(max_length=200, null=True)
    Quiz_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Quiz_name



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
    # Student_ID = models.IntegerField()
    Answer = models.CharField(max_length=200, null=True)
    Question_ID = models.ForeignKey(QuesModel, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(default = True)

class ResultModel(models.Model):
    #Student_ID
    Quiz_ID = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    Marks = models.IntegerField()