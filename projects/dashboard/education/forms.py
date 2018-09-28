from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from projects.education.models import (
    Student, EducationGroup, Teacher, Course, Lecture)
from projects.core.widgets import DatePickerInput

User = get_user_model()


class StudentForm(forms.ModelForm):
    original_user = forms.IntegerField(required=False)
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='dashboard:education-user-autocomplete',
            forward=('user', 'original_user',)))
    education_groups = forms.ModelMultipleChoiceField(
        queryset=EducationGroup.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='dashboard:education-group-autocomplete',
            forward=('education_groups',)))

    birth_date = forms.DateField(
        widget=DatePickerInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'no-widget-init'
        self.fields['education_groups'].widget.attrs['class'] = 'no-widget-init'
        self.fields['education_groups'].required = False
        self.fields['user'].required = False
        self.fields['original_user'].widget = forms.HiddenInput()
        if self.instance and self.instance.user:
            self.fields['original_user'].initial = self.instance.user.id

    class Meta:
        model = Student
        fields = '__all__'


class StudentSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=16, required=False, label='',
        widget=forms.TextInput(attrs={'placeholder': _('Last name')})
    )

    def clean(self):
        cleaned_data = super(StudentSearchForm, self).clean()
        cleaned_data['last_name'] = cleaned_data['last_name'].strip()
        return cleaned_data


class EducationGroupForm(forms.ModelForm):

    class Meta:
        model = EducationGroup
        fields = '__all__'


class EducationGroupSearchForm(forms.Form):
    name = forms.CharField(
        max_length=16, required=False, label='',
        widget=forms.TextInput(attrs={'placeholder': _('Name')})
    )

    def clean(self):
        cleaned_data = super(EducationGroupSearchForm, self).clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data


class TeacherForm(forms.ModelForm):
    original_user = forms.IntegerField(required=False)
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='dashboard:education-user-autocomplete',
            forward=('user', 'original_user',)))
    birth_date = forms.DateField(
        widget=DatePickerInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'no-widget-init'
        self.fields['user'].required = False
        self.fields['original_user'].widget = forms.HiddenInput()
        if self.instance and self.instance.user:
            self.fields['original_user'].initial = self.instance.user.id

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=16, required=False, label='',
        widget=forms.TextInput(attrs={'placeholder': _('Last name')})
    )

    def clean(self):
        cleaned_data = super(TeacherSearchForm, self).clean()
        cleaned_data['last_name'] = cleaned_data['last_name'].strip()
        return cleaned_data


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'


class CourseSearchForm(forms.Form):
    title = forms.CharField(
        max_length=16, required=False, label='',
        widget=forms.TextInput(attrs={'placeholder': _('Title')})
    )

    def clean(self):
        cleaned_data = super(CourseSearchForm, self).clean()
        cleaned_data['title'] = cleaned_data['title'].strip()
        return cleaned_data


class LectureForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='dashboard:education-course-autocomplete',
            forward=('course',)))
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='dashboard:education-teacher-autocomplete',
            forward=('teachers',)))
    groups = forms.ModelMultipleChoiceField(
        queryset=EducationGroup.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='dashboard:education-group-autocomplete',
            forward=('groups',)))
    start = forms.DateField(
        widget=DatePickerInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    finish = forms.DateField(
        widget=DatePickerInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)
        self.fields['course'].widget.attrs['class'] = 'no-widget-init'
        self.fields['teachers'].widget.attrs['class'] = 'no-widget-init'
        self.fields['groups'].widget.attrs['class'] = 'no-widget-init'
        self.fields['groups'].required = False

    class Meta:
        model = Lecture
        fields = '__all__'


class LectureSearchForm(forms.Form):
    title = forms.CharField(
        max_length=16, required=False, label='',
        widget=forms.TextInput(attrs={'placeholder': _('Title')})
    )

    def clean(self):
        cleaned_data = super(LectureSearchForm, self).clean()
        cleaned_data['title'] = cleaned_data['title'].strip()
        return cleaned_data
