from rest_framework import routers

# 
from .views import CategoriesViewSet,ActivityViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'', ActivityViewSet)
