from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    UserAutocomplete,
    StudentCreateView, StudentDeleteView,
    StudentListView, StudentUpdateView,
    EducationGroupAutocomplete, EducationGroupCreateView, EducationGroupDeleteView,
    EducationGroupListView, EducationGroupUpdateView,
    TeacherAutocomplete, TeacherCreateView, TeacherDeleteView,
    TeacherListView, TeacherUpdateView,
    CourseAutocomplete, CourseCreateView, CourseDeleteView,
    CourseListView, CourseUpdateView,
    LectureCreateView, LectureDeleteView,
    LectureListView, LectureUpdateView,
)


urlpatterns = [
    path(
        'users-autocomplete/', login_required(UserAutocomplete.as_view()),
        name='education-user-autocomplete'),
    path(
        'groups-autocomplete/', login_required(EducationGroupAutocomplete.as_view()),
        name='education-group-autocomplete'),
    path(
        'teachers-autocomplete/', login_required(TeacherAutocomplete.as_view()),
        name='education-teacher-autocomplete'),
    path(
        'courses-autocomplete/', login_required(CourseAutocomplete.as_view()),
        name='education-course-autocomplete'),
    path(
        'students/create/', login_required(StudentCreateView.as_view()),
        name='education-student-create'),
    path(
        'students/<int:pk>/update/', login_required(StudentUpdateView.as_view()),
        name='education-student-update'),
    path(
        'students/<int:pk>/delete/', login_required(StudentDeleteView.as_view()),
        name='education-student-delete'),
    path(
        'students/', login_required(StudentListView.as_view()),
        name='education-student-list'),

    path(
        'education-groups/create/', login_required(EducationGroupCreateView.as_view()),
        name='education-group-create'),
    path(
        'education-groups/<int:pk>/update/', login_required(EducationGroupUpdateView.as_view()),
        name='education-group-update'),
    path(
        'education-groups/<int:pk>/delete/', login_required(EducationGroupDeleteView.as_view()),
        name='education-group-delete'),
    path(
        'education-groups/', login_required(EducationGroupListView.as_view()),
        name='education-group-list'),

    path(
        'teachers/create/', login_required(TeacherCreateView.as_view()),
        name='education-teacher-create'),
    path(
        'teachers/<int:pk>/update/', login_required(TeacherUpdateView.as_view()),
        name='education-teacher-update'),
    path(
        'teachers/<int:pk>/delete/', login_required(TeacherDeleteView.as_view()),
        name='education-teacher-delete'),
    path(
        'teachers/', login_required(TeacherListView.as_view()),
        name='education-teacher-list'),

    path(
        'courses/create/', login_required(CourseCreateView.as_view()),
        name='education-course-create'),
    path(
        'courses/<int:pk>/update/', login_required(CourseUpdateView.as_view()),
        name='education-course-update'),
    path(
        'courses/<int:pk>/delete/', login_required(CourseDeleteView.as_view()),
        name='education-course-delete'),
    path(
        'courses/', login_required(CourseListView.as_view()),
        name='education-course-list'),

    path(
        'lectures/create/', login_required(LectureCreateView.as_view()),
        name='education-lecture-create'),
    path(
        'lectures/<int:pk>/update/', login_required(LectureUpdateView.as_view()),
        name='education-lecture-update'),
    path(
        'lectures/<int:pk>/delete/', login_required(LectureDeleteView.as_view()),
        name='education-lecture-delete'),
    path(
        'lectures/', login_required(LectureListView.as_view()),
        name='education-lecture-list'),
]
