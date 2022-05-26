from django.forms import ModelForm

from .models import *



class addQuizform(ModelForm):
    class Meta:
        model = QuizModel
        fields = ('Quiz_name',)



class addQuestionform(ModelForm):
    class Meta:
        model = QuesModel
        fields = "__all__"

class studentAnswerform(ModelForm):
    class Meta:
        model = AnswerModel
        fields = "__all__"
