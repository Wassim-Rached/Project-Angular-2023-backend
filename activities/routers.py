from rest_framework import routers

# 
from .views import CategoriesViewSet,ActivityViewSet,ActivityRegistrationViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'registrations', ActivityRegistrationViewSet)
router.register(r'', ActivityViewSet)
