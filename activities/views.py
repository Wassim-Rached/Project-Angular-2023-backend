from rest_framework import viewsets
from authentication.permissions import IsAdminOrReadOnly

from .models import Category,Activity
from .serializers import CategoriesSerializer,DetailActivitiesSerializer,ListActivitiesSerializer


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