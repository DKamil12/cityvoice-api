from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Reward, Product, Purchase
from .serializer import RewardSerializer, ProductSerializer, PurchaseSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions
from django.db.models import Sum
from rest_framework.decorators import action


# Create your views here.
class RewardViewSet(ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_reward(request):
    report_id = request.GET.get('report_id')
    exists = Reward.objects.filter(user=request.user, report_id=report_id).exists()
    return Response({'exists': exists})


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def balance(self, request):
        total = request.user.rewards.aggregate(total=Sum('amount'))['total'] or 0
        spent = request.user.purchases.aggregate(spent=Sum('product__price'))['spent'] or 0
        return Response({"balance": total - spent})

    @action(detail=False, methods=['post'])
    def purchase(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)  # проверка наличия товара
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        total = request.user.rewards.aggregate(total=Sum('amount'))['total'] or 0
        spent = request.user.purchases.aggregate(spent=Sum('product__price'))['spent'] or 0
        balance = total - spent  # получение текущего баланса пользователя

        if balance < product.price:
            return Response({'error': 'Недостаточно монет'}, status=status.HTTP_400_BAD_REQUEST)

        Purchase.objects.create(user=request.user, product=product)
        return Response({'success': 'Покупка успешно совершена'}, status=status.HTTP_201_CREATED)