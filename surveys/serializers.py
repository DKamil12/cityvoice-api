from rest_framework import serializers
from .models import SurveyQuestion, SurveyResponse
from reports.serializers import CategorySerializer
from reports.models import Category


class SurveyQuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = SurveyQuestion
        fields = ['id', 'text', 'is_active', 'category', 'category_id']


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['question', 'district', 'rating']
