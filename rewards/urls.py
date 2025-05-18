from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RewardViewSet, check_reward, ProductViewSet, ShopViewSet


router = DefaultRouter()
router.register(r'rewards', RewardViewSet)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'shop', ShopViewSet, basename='shop')

urlpatterns = [
    path('', include(router.urls)),
    path('check/', check_reward),
]