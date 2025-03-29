from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, BgImageViewSet

router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")
router.register(r"bgimages", BgImageViewSet, basename="bgimage")

urlpatterns = [
    path("", include(router.urls)),  # Include API routes
]
