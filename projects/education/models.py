from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    last_name = models.CharField(_('Last name'), max_length=200)
    first_name = models.CharField(_('First name'), max_length=200)
    birth_date = models.DateField(_('Birth date'))
    active = models.BooleanField(_('Status'), default=True)

    def __str__(self):
        return _(u'%(first_name)s %(last_name)s') % ({
            'first_name': self.first_name,
            'last_name': self.last_name}
        )

    class Meta:
        ordering = ['last_name']
        verbose_name = _('Student')
        verbose_name_plural = _('Students')


class EducationGroup(models.Model):
    users = models.ManyToManyField(Student, db_index=True)
    name = models.CharField(_('Name'), blank=False, max_length=200, db_index=True)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    last_name = models.CharField(_('Last name'), max_length=255)
    first_name = models.CharField(_('First name'), max_length=255)
    birth_date = models.DateField(_('Birth date'))
    active = models.BooleanField(_('Status'), default=True)

    def __str__(self):
        return _(u'%(first_name)s %(last_name)s') % ({
            'first_name': self.first_name,
            'last_name': self.last_name}
        )

    class Meta:
        ordering = ['last_name']
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')


class Course(models.Model):
    title = models.CharField(_('title'), blank=False, max_length=127)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class Lecture(models.Model):
    title = models.CharField(_('Title'), max_length=200, blank=False)
    description = models.TextField(_('Description'), blank=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    start = models.DateTimeField(_('Start'), null=False)
    finish = models.DateTimeField(_('finish'), null=False)
    teachers = models.ManyToManyField(Teacher)
    groups = models.ManyToManyField(EducationGroup)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Lecture')
        verbose_name_plural = _('Lecture')


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.course
