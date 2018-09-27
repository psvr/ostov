from django.urls import include, path
from django.contrib.auth.decorators import login_required

from .views import DashboardView

urlpatterns = [
    path('education/', include('projects.dashboard.education.urls')),
    path('', login_required(DashboardView.as_view()), name='home'),
]
