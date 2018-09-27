from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard/home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(DashboardView, self).dispatch(request, *args, **kwargs)
