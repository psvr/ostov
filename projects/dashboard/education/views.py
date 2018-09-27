from dal import autocomplete
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, UpdateView)
from django_tables2 import SingleTableView
from projects.education.models import (
    Student, EducationGroup, Teacher, Course, Lecture)

from .forms import (
    StudentForm, StudentSearchForm,
    EducationGroupForm, EducationGroupSearchForm,
    TeacherForm, TeacherSearchForm, CourseForm, CourseSearchForm,
    LectureForm, LectureSearchForm,
    )
from .tables import (
    StudentTable, EducationGroupTable, TeacherTable,
    CourseTable, LectureTable
    )

User = get_user_model()


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        qs = User.objects.filter(is_staff=False)

        user_id = self.forwarded.get('user_id', None)
        if user_id:
            qs = qs.exclude(id=user_id)

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs


class EducationGroupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return EducationGroup.objects.none()
        education_groups = self.forwarded.get('education_groups', None)

        if education_groups:
            qs = EducationGroup.objects.all().exclude(id__in=education_groups)
        else:
            qs = EducationGroup.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Teacher.objects.none()
        teachers = self.forwarded.get('teachers', None)

        if teachers:
            qs = Teacher.objects.all().exclude(id__in=teachers)
        else:
            qs = Teacher.objects.all()
        if self.q:
            qs = qs.filter(last_name__istartswith=self.q)
        return qs


class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.none()
        courses = self.forwarded.get('courses', None)

        if courses:
            qs = Course.objects.all().exclude(id__in=courses)
        else:
            qs = Course.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class StudentFilterMixin(object):
    model = Student

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(StudentFilterMixin, self).dispatch(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.request.user.is_staff:
            return qs
        return qs.none()

    def get_queryset(self):
        return self.filter_queryset(
            super(StudentFilterMixin, self).get_queryset())

    def get_success_url(self):
        return reverse('dashboard:education-student-list')


class StudentListView(StudentFilterMixin, SingleTableView):
    template_name = 'dashboard/education/student/list.html'
    form_class = StudentSearchForm
    table_class = StudentTable
    context_table_name = 'students'

    def get_context_data(self, **kwargs):
        ctx = super(StudentListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        qs = super(StudentListView, self).get_queryset()
        qs = self.apply_search(qs)
        return qs

    def apply_search(self, queryset):
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data
        if data.get('last_name'):
            queryset = queryset.filter(last_name__icontains=data['last_name'])

        return queryset


class StudentDeleteView(StudentFilterMixin, DeleteView):
    template_name = 'dashboard/education/student/delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(StudentDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Student deleted successfully'))
        return super(StudentDeleteView, self).get_success_url()


class StudentCreateView(StudentFilterMixin, CreateView):
    template_name = 'dashboard/education/student/form.html'
    form_class = StudentForm

    def get_context_data(self, **kwargs):
        ctx = super(StudentCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Add a new student')
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Student created successfully'))
        return super(StudentCreateView, self).get_success_url()

    def get_initial(self):
        initial = super(StudentCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class StudentUpdateView(StudentFilterMixin, UpdateView):
    template_name = 'dashboard/education/student/form.html'
    form_class = StudentForm

    def get_context_data(self, **kwargs):
        ctx = super(StudentUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Update student: %s') % self.object
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Student updated successfully'))
        return super(StudentUpdateView, self).get_success_url()


class EducationGroupFilterMixin(object):
    model = EducationGroup

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(EducationGroupFilterMixin, self).dispatch(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.request.user.is_staff:
            return qs
        return qs.none()

    def get_queryset(self):
        return self.filter_queryset(
            super(EducationGroupFilterMixin, self).get_queryset())

    def get_success_url(self):
        return reverse('dashboard:education-group-list')


class EducationGroupListView(EducationGroupFilterMixin, SingleTableView):
    template_name = 'dashboard/education/group/list.html'
    form_class = EducationGroupSearchForm
    table_class = EducationGroupTable
    context_table_name = 'groups'

    def get_context_data(self, **kwargs):
        ctx = super(EducationGroupListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        qs = super(EducationGroupListView, self).get_queryset()
        qs = self.apply_search(qs)
        return qs

    def apply_search(self, queryset):
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data
        if data.get('name'):
            queryset = queryset.filter(name__icontains=data['name'])

        return queryset


class EducationGroupDeleteView(EducationGroupFilterMixin, DeleteView):
    template_name = 'dashboard/education/group/delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(EducationGroupDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Education Group deleted successfully'))
        return super(EducationGroupDeleteView, self).get_success_url()


class EducationGroupCreateView(EducationGroupFilterMixin, CreateView):
    template_name = 'dashboard/education/group/form.html'
    form_class = EducationGroupForm

    def get_context_data(self, **kwargs):
        ctx = super(EducationGroupCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Add a new group')
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Education Group created successfully'))
        return super(EducationGroupCreateView, self).get_success_url()

    def get_initial(self):
        initial = super(EducationGroupCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class EducationGroupUpdateView(EducationGroupFilterMixin, UpdateView):
    template_name = 'dashboard/education/group/form.html'
    form_class = EducationGroupForm

    def get_context_data(self, **kwargs):
        ctx = super(EducationGroupUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Update group: %s') % self.object
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Education Group updated successfully'))
        return super(EducationGroupUpdateView, self).get_success_url()


class TeacherFilterMixin(object):
    model = Teacher

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(TeacherFilterMixin, self).dispatch(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.request.user.is_staff:
            return qs
        return qs.none()

    def get_queryset(self):
        return self.filter_queryset(
            super(TeacherFilterMixin, self).get_queryset())

    def get_success_url(self):
        return reverse('dashboard:education-teacher-list')


class TeacherListView(TeacherFilterMixin, SingleTableView):
    template_name = 'dashboard/education/teacher/list.html'
    form_class = TeacherSearchForm
    table_class = TeacherTable
    context_table_name = 'teachers'

    def get_context_data(self, **kwargs):
        ctx = super(TeacherListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        qs = super(TeacherListView, self).get_queryset()
        qs = self.apply_search(qs)
        return qs

    def apply_search(self, queryset):
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data
        if data.get('last_name'):
            queryset = queryset.filter(last_name__icontains=data['last_name'])

        return queryset


class TeacherDeleteView(TeacherFilterMixin, DeleteView):
    template_name = 'dashboard/education/teacher/delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(TeacherDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Teacher deleted successfully'))
        return super(TeacherDeleteView, self).get_success_url()


class TeacherCreateView(TeacherFilterMixin, CreateView):
    template_name = 'dashboard/education/teacher/form.html'
    form_class = TeacherForm

    def get_context_data(self, **kwargs):
        ctx = super(TeacherCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Add a new teacher')
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Teacher created successfully'))
        return super(TeacherCreateView, self).get_success_url()

    def get_initial(self):
        initial = super(TeacherCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class TeacherUpdateView(TeacherFilterMixin, UpdateView):
    template_name = 'dashboard/education/teacher/form.html'
    form_class = TeacherForm

    def get_context_data(self, **kwargs):
        ctx = super(TeacherUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Update teacher: %s') % self.object
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Teacher updated successfully'))
        return super(TeacherUpdateView, self).get_success_url()


class CourseFilterMixin(object):
    model = Course

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(CourseFilterMixin, self).dispatch(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.request.user.is_staff:
            return qs
        return qs.none()

    def get_queryset(self):
        return self.filter_queryset(
            super(CourseFilterMixin, self).get_queryset())

    def get_success_url(self):
        return reverse('dashboard:education-course-list')


class CourseListView(CourseFilterMixin, SingleTableView):
    template_name = 'dashboard/education/course/list.html'
    form_class = CourseSearchForm
    table_class = CourseTable
    context_table_name = 'courses'

    def get_context_data(self, **kwargs):
        ctx = super(CourseListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        qs = super(CourseListView, self).get_queryset()
        qs = self.apply_search(qs)
        return qs

    def apply_search(self, queryset):
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data
        if data.get('title'):
            queryset = queryset.filter(title__icontains=data['title'])

        return queryset


class CourseDeleteView(CourseFilterMixin, DeleteView):
    template_name = 'dashboard/education/course/delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(CourseDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Course deleted successfully'))
        return super(CourseDeleteView, self).get_success_url()


class CourseCreateView(CourseFilterMixin, CreateView):
    template_name = 'dashboard/education/course/form.html'
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        ctx = super(CourseCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Add a new course')
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Course created successfully'))
        return super(CourseCreateView, self).get_success_url()

    def get_initial(self):
        initial = super(CourseCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class CourseUpdateView(CourseFilterMixin, UpdateView):
    template_name = 'dashboard/education/course/form.html'
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        ctx = super(CourseUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Update course: %s') % self.object
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Course updated successfully'))
        return super(CourseUpdateView, self).get_success_url()


class LectureFilterMixin(object):
    model = Lecture

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(LectureFilterMixin, self).dispatch(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.request.user.is_staff:
            return qs
        return qs.none()

    def get_queryset(self):
        return self.filter_queryset(
            super(LectureFilterMixin, self).get_queryset())

    def get_success_url(self):
        return reverse('dashboard:education-lecture-list')


class LectureListView(LectureFilterMixin, SingleTableView):
    template_name = 'dashboard/education/lecture/list.html'
    form_class = LectureSearchForm
    table_class = LectureTable
    context_table_name = 'lectures'

    def get_context_data(self, **kwargs):
        ctx = super(LectureListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        qs = super(LectureListView, self).get_queryset()
        qs = self.apply_search(qs)
        return qs

    def apply_search(self, queryset):
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data
        if data.get('title'):
            queryset = queryset.filter(title__icontains=data['title'])

        return queryset


class LectureDeleteView(LectureFilterMixin, DeleteView):
    template_name = 'dashboard/education/lecture/delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(LectureDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Lecture deleted successfully'))
        return super(LectureDeleteView, self).get_success_url()


class LectureCreateView(LectureFilterMixin, CreateView):
    template_name = 'dashboard/education/lecture/form.html'
    form_class = LectureForm

    def get_context_data(self, **kwargs):
        ctx = super(LectureCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Add a new lecture')
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Lecture created successfully'))
        return super(LectureCreateView, self).get_success_url()

    def get_initial(self):
        initial = super(LectureCreateView, self).get_initial()
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class LectureUpdateView(LectureFilterMixin, UpdateView):
    template_name = 'dashboard/education/lecture/form.html'
    form_class = LectureForm

    def get_context_data(self, **kwargs):
        ctx = super(LectureUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Update lecture: %s') % self.object
        return ctx

    def get_success_url(self):
        messages.info(self.request, _('Lecture updated successfully'))
        return super(LectureUpdateView, self).get_success_url()
