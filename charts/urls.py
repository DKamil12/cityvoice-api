from rest_framework.urls import path
from .views import ReportsByCategoryView, ReportsByDistrictView, DistrictCategoryStatsView


urlpatterns = [
    path('reports-by-category/', ReportsByCategoryView.as_view()),
    # path('reports-by-district/', ReportsByDistrictView.as_view()),
    path("reports-by-district/<int:district_id>/stats/", DistrictCategoryStatsView.as_view()),
]
