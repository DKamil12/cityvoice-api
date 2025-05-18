from django.db import models
from reports.models import District
from django.contrib.auth.models import User


class SurveyQuestion(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)


class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
