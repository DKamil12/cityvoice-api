from django.db import models
from django.contrib.auth.models import User
from reports.models import Report

# Create your models here.
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='rewards')
    amount = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'report')  # Один пользователь за одну заявку - одна награда
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.amount} баллов за успешное завершение заявки {self.report.id}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} купил {self.product.name}"