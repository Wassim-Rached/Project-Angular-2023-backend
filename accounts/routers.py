from rest_framework import routers

#
from .views import CustomUserViewSet, AccountViewSet, JoinClubFormViewSet

router = routers.DefaultRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"join_us", JoinClubFormViewSet)
router.register(r"", AccountViewSet)
