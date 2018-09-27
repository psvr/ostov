from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EducationConfig(AppConfig):
    label = 'dashboard_education'
    name = 'projects.dashboard.education'
    verbose_name = _('Educations')
