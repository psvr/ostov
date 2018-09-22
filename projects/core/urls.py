from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .forms import CustomAuthenticationForm


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name="core/login.html", authentication_form=CustomAuthenticationForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', login_required(TemplateView.as_view(template_name='dashboard/index.html')), name='index')
]
