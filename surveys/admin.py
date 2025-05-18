from django.contrib import admin
from .models import SurveyQuestion, SurveyResponse

admin.site.register(SurveyResponse)
admin.site.register(SurveyQuestion)

# Register your models here.
