from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ReportViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('reports/', include(router.urls))
]