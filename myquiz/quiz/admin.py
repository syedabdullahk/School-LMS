from django.contrib import admin
from .models import *


# Register your models here.
class QuizAdmin(admin.ModelAdmin):
	list_display = ('question',)


admin.site.register(QuesModel)
admin.site.register(QuizModel)