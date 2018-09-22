from django.urls import include, path

handler403 = 'projects.core.views.handle_403'
handler404 = 'projects.core.views.handle_404'
handler500 = 'projects.core.views.handle_500'

urlpatterns = [
    path('', include(('projects.core.urls', 'core'), namespace='core')),
]
