from rest_framework.routers import DefaultRouter
from .views import ProviderViewSet, ServiceAreaViewSet


router = DefaultRouter()

router.register(r'providers', ProviderViewSet)
router.register(r'service-areas', ServiceAreaViewSet)

urlpatterns = router.urls
