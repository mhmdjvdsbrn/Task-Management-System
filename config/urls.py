from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('admin/', admin.site.urls),
    path('api/auth/', include(('task_backend.authentication.urls', 'auth'))),
    path('api/users/', include(('task_backend.users.urls', 'register'))),
    path('api/', include('task_backend.projects.urls')),  # Adjust the path as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # ... your other URL patterns ...
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns