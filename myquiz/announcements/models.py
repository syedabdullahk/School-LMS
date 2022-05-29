from django.db import models
from django.utils import timezone
from users.models import User
from courses.models import Course

from django.urls import reverse

# Create your models here.
class Announcement(models.Model):
    subject = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name="announcement", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="course_announcement", on_delete=models.CASCADE)
    is_general = models.BooleanField(default = False)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('quiz:home')


