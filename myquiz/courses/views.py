

from django.views import generic

from courses.models import Course, Enrollment
from assignment.models import Assignment
# Create your views here.
class CourseDetail(generic.DetailView):
    model = Course

    def get_context_data(self,**kwargs):
        assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['assignments'] = assignments
        return context

class CourseListView(generic.ListView):
    model = Course
   # courses = Course.objects.filter()