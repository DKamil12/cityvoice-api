from django.urls import path
from .views import SurveyQuestionListView, SurveyResponseCreateView, SurveyAvailabilityAPIView

urlpatterns = [
    path('questions/', SurveyQuestionListView.as_view()), 
    path('submit/', SurveyResponseCreateView.as_view()), 
    path('available/', SurveyAvailabilityAPIView.as_view()), 
]
