from django.db import models
from django.utils import timezone
from users.models import User

from django.urls import reverse

# Create your models here.
class Announcement(models.Model):
    subject = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name="announcement", on_delete=models.CASCADE)
    # add a course id

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('quiz:home')


