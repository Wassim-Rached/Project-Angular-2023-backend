from django_filters import rest_framework as filters
from .models import ActivityRegistration


class ActivityRegistrationFilterClass(filters.FilterSet):
    class Meta:
        model = ActivityRegistration
        fields = ["status", "is_payed"]
