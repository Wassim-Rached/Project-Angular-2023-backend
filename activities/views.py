from authentication.permissions import IsAdminOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, filters, permissions

from django.db.models import Count

from .filters import ActivityRegistrationFilterClass
from .permissions import IsObjectOwnerOrAdminPermission
from .models import Category, Activity, ActivityRegistration
from .serializers import (
    CategoriesSerializer,
    DetailActivitiesSerializer,
    ListActivitiesSerializer,
    NonAdminActivityRegistrationSerializer,
    AdminActivityRegistrationSerializer,
    CreateActivitiesSerializer,
    UpdateActivitiesSerializer,
    SimpleCategorySerializer,
)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {"name": ["icontains"]}
    ordering_fields = ["popular"]

    def get_serializer_class(self):
        if self.action == "list":
            return SimpleCategorySerializer

        return CategoriesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(popular=Count("activities"))
        return queryset


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ListActivitiesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "title": ["icontains"],
        "categories__name": ["exact"],
        "is_free": ["exact"],
    }
    ordering_fields = ["created_at", "likes_count"]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(likes_count=Count("likes"))
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ListActivitiesSerializer

        if self.action in ["update", "partial_update"]:
            print("update serializer")
            return UpdateActivitiesSerializer

        if self.action in ["create"]:
            return CreateActivitiesSerializer

        return DetailActivitiesSerializer

    @action(
        detail=True,
        methods=["POST"],
        url_name="toogle-like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def toogle_like(self, request, pk=None):
        activity = self.get_object()
        account = request.user.account
        activity.toogle_like(account)
        return Response({"is_liked": activity.isLikedBy(request.user.account)})

    @action(
        detail=True,
        methods=["POST"],
        url_name="like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request, pk=None):
        activity = self.get_object()
        account = request.user.account
        liked = activity.isLikedBy(account)
        if not liked:
            activity.like(account)
        return Response({"have_changed": not liked})

    @action(
        detail=True,
        methods=["GET"],
        url_name="did-like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def did_like(self, request, pk=None):
        activity = self.get_object()
        account = request.user.account
        liked = activity.isLikedBy(account)
        return Response({"did_like": liked})

    @action(
        detail=True,
        methods=["GET"],
        url_name="get-related-registrations",
        permission_classes=[permissions.IsAuthenticated],
    )
    def registrations(self, request, pk):
        activity = self.get_object()
        activityRegistration = ActivityRegistration.objects.filter(activity=activity)

        filterset = ActivityRegistrationFilterClass(
            request.GET, queryset=activityRegistration
        )
        filtered_queryset = filterset.qs

        ordered_queryset = self.ordering(request, filtered_queryset, self)

        instance = AdminActivityRegistrationSerializer(ordered_queryset, many=True)

        return Response(instance.data)

    @action(
        detail=True,
        methods=["GET"],
        url_name="activity-categories",
        permission_classes=[permissions.AllowAny],
    )
    def categories(self, request, pk=None):
        activity = self.get_object()
        instance = SimpleCategorySerializer(activity.categories, many=True)
        return Response({"categories": instance.data})


class ActivityRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ActivityRegistration.objects.all()
    serializer_class = NonAdminActivityRegistrationSerializer
    permission_classes = [IsObjectOwnerOrAdminPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "status": ["exact"],
        "is_payed": ["exact"],
    }
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return super().get_queryset()
        else:
            return ActivityRegistration.objects.filter(account=user.account)

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return AdminActivityRegistrationSerializer

        return NonAdminActivityRegistrationSerializer

    def update(self, request, *args, **kwargs):
        # Raise a MethodNotAllowed exception with a custom error message
        raise MethodNotAllowed("Updates are not allowed for ActivityRegistrations.")

    @action(
        detail=True,
        methods=["POST"],
        url_name="accept",
        permission_classes=[IsAdminUser],
    )
    def accept(self, request, pk=None):
        activity_registration = self.get_object()
        activity_registration.acceptActivitieRegistration()
        return Response({"status": activity_registration.status})

    @action(
        detail=True,
        methods=["POST"],
        url_name="reject",
        permission_classes=[IsAdminUser],
    )
    def reject(self, request, pk=None):
        activity_registration = self.get_object()
        activity_registration.rejectActivitieRegistration()
        return Response({"status": activity_registration.status})

    @action(
        detail=True, methods=["POST"], url_name="pay", permission_classes=[IsAdminUser]
    )
    def pay(self, request, pk=None):
        activity_registration = self.get_object()
        activity_registration.payRegistration()
        return Response({"is_payed": activity_registration.is_payed})

    @action(
        detail=True,
        methods=["POST"],
        url_name="unpay",
        permission_classes=[IsAdminUser],
    )
    def unpay(self, request, pk=None):
        activity_registration = self.get_object()
        activity_registration.unPayRegistration()
        return Response({"is_payed": activity_registration.is_payed})
