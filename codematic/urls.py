from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Codematic Films",
        default_version='v1',
        description="List of Films and comments",
        terms_of_service="codematic.com",
        contact=openapi.Contact(email="contact@codematic.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
)


urlpatterns = [
    path('', include('film.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='documentation-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
