from django.urls import path
from .views import SurveyQuestionListView, SurveyResponseCreateView, SurveyStatisticsView, SurveyAvailabilityAPIView, CitywideSurveyStatsView

urlpatterns = [
    path('questions/', SurveyQuestionListView.as_view()),
    path('submit/', SurveyResponseCreateView.as_view()),
    path('available/', SurveyAvailabilityAPIView.as_view()),
    path('statistics/', SurveyStatisticsView.as_view()),
    path('statistics/citywide/', CitywideSurveyStatsView.as_view(), name='citywide-survey-stats'),
]
