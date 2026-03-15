from rest_framework.routers import DefaultRouter

from rides.views import RideViewSet

router = DefaultRouter()
router.register(r'', RideViewSet, basename='rides')

urlpatterns = router.urls
