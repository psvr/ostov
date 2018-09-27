from django.utils.translation import ungettext_lazy
from django_tables2 import A, LinkColumn, TemplateColumn
from projects.education.models import (
    Student, EducationGroup, Teacher, Course, Lecture)
from projects.dashboard.tables import DashboardTable


class StudentTable(DashboardTable):
    last_name = LinkColumn('dashboard:education-student-update', args=[A('pk')])
    actions = TemplateColumn(
        template_name='dashboard/education/student/row_actions.html',
        orderable=False)

    icon = 'sitemap'
    caption = ungettext_lazy('%s Student', '%s Students')

    class Meta(DashboardTable.Meta):
        model = Student
        fields = ('last_name', 'first_name', 'user', 'birth_date', 'active')
        order_by = 'last_name'


class EducationGroupTable(DashboardTable):
    name = LinkColumn('dashboard:education-group-update', args=[A('pk')])
    actions = TemplateColumn(
        template_name='dashboard/education/group/row_actions.html',
        orderable=False)

    icon = 'sitemap'
    caption = ungettext_lazy('%s Group', '%s Groups')

    class Meta(DashboardTable.Meta):
        model = EducationGroup
        fields = ('name', 'active')
        order_by = 'name'


class TeacherTable(DashboardTable):
    last_name = LinkColumn('dashboard:education-teacher-update', args=[A('pk')])
    actions = TemplateColumn(
        template_name='dashboard/education/teacher/row_actions.html',
        orderable=False)

    icon = 'sitemap'
    caption = ungettext_lazy('%s Teacher', '%s Teachers')

    class Meta(DashboardTable.Meta):
        model = Teacher
        fields = ('last_name', 'first_name', 'user', 'birth_date', 'active')
        order_by = 'last_name'


class CourseTable(DashboardTable):
    title = LinkColumn('dashboard:education-course-update', args=[A('pk')])
    actions = TemplateColumn(
        template_name='dashboard/education/course/row_actions.html',
        orderable=False)

    icon = 'sitemap'
    caption = ungettext_lazy('%s Course', '%s Courses')

    class Meta(DashboardTable.Meta):
        model = Course
        fields = ('title', 'active')
        order_by = 'title'


class LectureTable(DashboardTable):
    title = LinkColumn('dashboard:education-lecture-update', args=[A('pk')])
    actions = TemplateColumn(
        template_name='dashboard/education/lecture/row_actions.html',
        orderable=False)

    icon = 'sitemap'
    caption = ungettext_lazy('%s Lecture', '%s Lectures')

    class Meta(DashboardTable.Meta):
        model = Lecture
        fields = ('title', 'course', 'start', 'finish')
        order_by = 'title'
