from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ReportViewSet, CommentViewSet, DistrictViewSet, MyReportsView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'comments', CommentViewSet)
router.register('districts', DistrictViewSet)

urlpatterns = [
    path('reports/', include(router.urls)),
    path('reports/my-reports/', MyReportsView.as_view()),
]