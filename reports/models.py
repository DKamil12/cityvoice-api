from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В процессе'),
        ('resolved', 'Решение'),
        ('rejected', 'Отклонено')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    latitude = models.FloatField(null=True)
    longtitude = models.FloatField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.pk} - {self.status}"
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
