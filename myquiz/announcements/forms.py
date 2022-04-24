from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import *



class CreateAnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ('subject', 'body')
     #   labels = {
       #     'due_date': 'Due Date (yyyy-mm-dd HH:MM)'
       # }

