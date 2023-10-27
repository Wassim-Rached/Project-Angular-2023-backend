from rest_framework import viewsets
from rest_framework.decorators import action,permission_classes
from authentication.permissions import IsAdminOrReadOnly,IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsObjectOwnerOrAdminPermission
from .models import Category,Activity,ActivityRegistration
from .serializers import CategoriesSerializer,DetailActivitiesSerializer,ListActivitiesSerializer,NonAdminActivityRegistrationSerializer,AdminActivityRegistrationSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategoriesSerializer
	permission_classes = [IsAdminOrReadOnly]


class ActivityViewSet(viewsets.ModelViewSet):
	queryset = Activity.objects.all()
	permission_classes = [IsAdminOrReadOnly]
	serializer_class = ListActivitiesSerializer

	def get_serializer_class(self):
		if self.action == 'list':
			return ListActivitiesSerializer
		return DetailActivitiesSerializer
	
	@action(detail=True, methods=['POST'], url_name='toogle-like', permission_classes=[IsAdminUser])
	def toogle_like(self, request, pk=None):
		activity = self.get_object()
		account = request.user.account
		activity.toogle_like(account)
		return Response({"is_liked": activity.isLikedBy(request.user.account)})


class ActivityRegistrationViewSet(viewsets.ModelViewSet):
	queryset = ActivityRegistration.objects.all()
	serializer_class = NonAdminActivityRegistrationSerializer
	permission_classes = [IsObjectOwnerOrAdminPermission]


	def get_queryset(self):
		user = self.request.user
		if user.is_admin:
			return ActivityRegistration.objects.all()
		else:
			return ActivityRegistration.objects.filter(account=user.account)


	def get_serializer_class(self):
		if self.request.user.is_admin:
			return AdminActivityRegistrationSerializer
		
		return NonAdminActivityRegistrationSerializer


	def update(self, request, *args, **kwargs):
		if not self.request.user.is_admin:
			return Response(
                {"detail": "Non-admin users are not allowed to update ActivityRegistrations."},
				status=status.HTTP_403_FORBIDDEN
			)
		
		return super().update(request, *args, **kwargs)

	@action(detail=True, methods=['POST'], url_name='accept', permission_classes=[IsAdminUser])
	def accept(self, request, pk=None):
		activity_registration = self.get_object()
		activity_registration.acceptActivitieRegistration()
		return Response({"status": activity_registration.status})

	@action(detail=True, methods=['POST'], url_name='reject', permission_classes=[IsAdminUser])
	def reject(self, request, pk=None):
		activity_registration = self.get_object()
		activity_registration.rejectActivitieRegistration()
		return Response({"status": activity_registration.status})
	
	@action(detail=True, methods=['POST'], url_name='pay', permission_classes=[IsAdminUser])
	def pay(self, request, pk=None):
		activity_registration = self.get_object()
		activity_registration.payRegistration()
		return Response({"is_payed": activity_registration.is_payed})

	@action(detail=True, methods=['POST'], url_name='unpay', permission_classes=[IsAdminUser])
	def unpay(self, request, pk=None):
		activity_registration = self.get_object()
		activity_registration.unPayRegistration()
		return Response({"is_payed": activity_registration.is_payed})
