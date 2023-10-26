from rest_framework import routers

# 
from .views import CustomUserViewSet,AccountViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'', AccountViewSet)