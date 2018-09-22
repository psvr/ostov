from django.template.response import TemplateResponse


def handle_403(request, exception=None):
    return TemplateResponse(request, '403.html', status=403)


def handle_404(request, exception=None):
    return TemplateResponse(request, '404.html', status=404)


def handle_500(request, exception=None):
    return TemplateResponse(request, '500.html', status=500)
