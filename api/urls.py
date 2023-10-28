from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import AccountPhotoView, ActivityPhotoView


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="backend for angular project @isetcharguia by wassim rached & chaima chouikh",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="wassimrached404@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("authentication/", include("authentication.urls")),
    path("activities/", include("activities.urls")),
    #
    path(
        "photo/account/<uuid:pk>/",
        AccountPhotoView.as_view(),
        name="account-photo-detail",
    ),
    path(
        "photo/activity/<uuid:pk>/",
        ActivityPhotoView.as_view(),
        name="activity-photo-detail",
    ),
    #
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
