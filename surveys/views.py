from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Avg
from .models import SurveyQuestion, SurveyResponse
from .serializers import SurveyQuestionSerializer, SurveyResponseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class SurveyQuestionListView(generics.ListAPIView):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer

class SurveyResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question_id = request.data.get("question")
        rating = request.data.get("rating")
        district_id = request.data.get("district")

        if not all([question_id, rating, district_id]):
            raise ValidationError("Не все поля заполнены")

        if SurveyResponse.objects.filter(user=request.user, question_id=question_id).exists():
            raise ValidationError("Вы уже проходили этот опрос")

        SurveyResponse.objects.create(
            user=request.user,
            question_id=question_id,
            rating=rating,
            district_id=district_id,
        )
        return Response({"success": True})
    

class SurveyAvailabilityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_questions = SurveyQuestion.objects.count()
        user_answers = SurveyResponse.objects.filter(user=request.user).values('question_id').distinct().count()
        available = user_answers < total_questions
        return Response({"available": available})
