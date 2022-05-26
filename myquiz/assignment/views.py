from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os
from django.conf import settings

# from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)


# Create your views here.



class CreateAssignment2(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAssignmentForm
    template_name = 'assignment/createAssignment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SubmitAssignmentView(LoginRequiredMixin, generic.CreateView):
    form_class = SubmitAssignmentForm
    template_name = 'assignment/submitassignment_form.html'
    select_related = ('author', 'assignment_ques')

    # success_url = reverse('assignments:submit_detail')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        assignments = Assignment.objects.get(pk=self.request.session.get('assignment'))
        obj.assignment_ques = assignments
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        assignments = Assignment.objects.filter(pk=self.request.session.get('assignment'))
        assignment_object = get_object_or_404(assignments)
        context = super(SubmitAssignmentView, self).get_context_data(**kwargs)
        context['duedate'] = assignment_object.due_date
        context['time'] = timezone.now()
        return context



class SubmitAssignmentDetail(LoginRequiredMixin, generic.DetailView):
    model = SubmitAssignment
    template_name = 'assignment/assignment_submissions.html'

    def get_context_data(self, **kwargs):
        submissions = SubmitAssignment.objects.filter(pk=self.kwargs['pk'])
        submissions_object = get_object_or_404(submissions)
        context = super(SubmitAssignmentDetail, self).get_context_data(**kwargs)
        context['submissions'] = submissions_object
        return context


class AssignmentDetail(LoginRequiredMixin, generic.DetailView,generic.FormView):
    model = Assignment
    form_class = SubmitAssignmentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        assignments = Assignment.objects.get(pk=self.request.session.get('assignment'))
        obj.assignment_ques = assignments
        obj.submitted_date = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # course_obj = Course.objects.filter(students=self.request.user.id)
        context = super(AssignmentDetail, self).get_context_data(**kwargs)
        # context['course'] = course_obj
        assignment = Assignment.objects.filter(pk=self.kwargs['pk'])
        assignment_object = get_object_or_404(assignment)
        context['duedate'] = assignment_object.due_date
        context['time'] = timezone.now()
        submitassignment = SubmitAssignment.objects.filter(assignment_ques=self.kwargs['pk'])
        context['submitted'] = submitassignment
        self.request.session['assignment'] = self.kwargs['pk']
        # print(self.request.session['assignment'])
        return context


class AssignmentListView(generic.ListView):
    model = Assignment

    def get_context_data(self, **kwargs):

        context = super(AssignmentListView, self).get_context_data(**kwargs)
        filtered_assignments = Assignment.objects.filter(course=self.kwargs['pk'])
        context['object_list'] = filtered_assignments
        return context

    # the default template is (lowercase)<modelname>_list
class AssignmentSubmitDetail(LoginRequiredMixin, generic.DetailView,generic.FormView):

    model = SubmitAssignment

