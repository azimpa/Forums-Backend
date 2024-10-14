from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ThreadViewSet, ResponseViewSet, TagViewSet

router = DefaultRouter()

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'threads', ThreadViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls
