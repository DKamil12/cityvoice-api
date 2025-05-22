from django.db import models
from reports.models import District
from django.contrib.auth.models import User
from reports.models import Category


class SurveyQuestion(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
