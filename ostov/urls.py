from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


handler403 = 'projects.core.views.handle_403'
handler404 = 'projects.core.views.handle_404'
handler500 = 'projects.core.views.handle_500'

urlpatterns = [
    path('dashboard/', include(('projects.dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('', include(('projects.core.urls', 'core'), namespace='core')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
