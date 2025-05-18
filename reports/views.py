from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.dateparse import parse_date

from rest_framework import viewsets
from rest_framework.response import Response

from django.contrib.gis.geos import Point

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from .serializers import CategorySerializer, ReportOnCreateSerializer, ReportOnReadSerializer, ReportOnUpdateSerializer, CommentSerializerOnRead, CommentSerializerOnWrite, DistrictSerializer
from .models import Category, Report, Comments, District

from rewards.models import Reward

# Create your views here.
class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Представление для взаимодействия с категориями. 

    HTTP действия: GET, POST, PUT, DELETE
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ReportViewSet(viewsets.ModelViewSet):
    """
    Представление для взаимодействия с жалобами. 

    HTTP действия: GET, POST, PUT, DELETE
    """
    queryset = Report.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'district', 'status']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ReportOnCreateSerializer
        elif self.action == 'update':
            return ReportOnUpdateSerializer
        return ReportOnReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(created_at__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created_at__lte=parse_date(end_date))

        return queryset

    def perform_create(self, serializer):
        lat = self.request.data.get('latitude')
        lon = self.request.data.get('longtitude')
        point = Point(float(lon), float(lat))
        district = District.objects.filter(geometry__contains=point).first()

        serializer.save(user=self.request.user, district=district)

    def update(self, request, *args, **kwargs):
        report = self.get_object()
        user = request.user
        status = request.data.get('status')
        comment_text = request.data.get('comment')

        if not user.is_staff:
            raise PermissionDenied('Только исполнители могут изменять статус жалобы!')
        if not comment_text:
            raise ValidationError('Перед обновлением статуса оставьте комментарий!')

        was_completed = report.status == 'resolved'
        report.status = status
        report.save()
        Comments.objects.create(user=user, report=report, text=comment_text)

        if status == 'resolved' and not was_completed:
            Reward.objects.get_or_create(
                user=report.user,
                report=report,
                defaults={'amount': 100}
            )

        return Response(ReportOnReadSerializer(report).data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для взаимодействия с комментариями. 

    HTTP действия: GET, POST, PUT, DELETE
    """
    queryset = Comments.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CommentSerializerOnWrite
        else:
            return CommentSerializerOnRead

    def perform_create(self, serializer):
        report = serializer.validated_data['report']
        user = self.request.user

        if user != report.user or not user.is_staff:
            raise PermissionDenied('Только исполнитель и владелец жалобы могут оставлять комментарии!')
        
        serializer.save(user=user)