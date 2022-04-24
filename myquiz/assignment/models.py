from django.db import models
from django.utils import timezone
from users.models import User

from django.urls import reverse

# Create your models here.
class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200, blank=False)
    assignment_description = models.TextField(blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True)
    # add a course id

    def __str__(self):
        return self.assignment_name

    def get_absolute_url(self):
        return reverse('assignment:detail', kwargs={'pk': self.pk})



class SubmitAssignment(models.Model):
    author = models.ForeignKey(User, related_name='assignment', on_delete=models.CASCADE)
   # assignment_name = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assignment_file = models.FileField(blank=False)
    submitted_date = models.DateTimeField(default=timezone.now)
    assignment_ques = models.ForeignKey(Assignment, related_name="question", on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('quiz:home')