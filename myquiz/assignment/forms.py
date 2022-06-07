from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django import forms
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from .models import *


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'




class CreateAssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_name', 'assignment_description',
                  'due_date')
        widgets = {

            'due_date': DateTimePickerInput(),
        }
     #   labels = {
       #     'due_date': 'Due Date (yyyy-mm-dd HH:MM)'
       # }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username=user.username)
        new_user_object = get_object_or_404(user_object)




class SubmitAssignmentForm(ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ('assignment_file',)

    '''''''''
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        assignment = kwargs.pop('assignment_id')
        super().__init__(*args, **kwargs)
        #self.fields['assignment_ques'].queryset = self.fields['assignment_ques'].queryset.filter(pk=assignment)
       # self.fields['author'].queryset = self.fields['author'].queryset.filter(username=user.username)
       
    '''''''''