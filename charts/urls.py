from rest_framework.urls import path
from .views import ReportsByCategoryView


urlpatterns = [
    path('reports-by-category/', ReportsByCategoryView.as_view()),
]