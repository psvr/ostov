from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from .forms import CustomAuthenticationForm


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name="core/login.html", authentication_form=CustomAuthenticationForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', RedirectView.as_view(pattern_name='dashboard:home', permanent=False), name="index")
]
