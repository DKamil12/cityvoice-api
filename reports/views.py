from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import CategorySerializer, ReportOnCreateSerializer, ReportOnReadSerializer, ReportOnUpdateSerializer, CommentSerializerOnRead, CommentSerializerOnWrite
from .models import Category, Report, Comments

# Create your views here.
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return ReportOnCreateSerializer
        elif self.action == 'update':
            return ReportOnUpdateSerializer
        else:
            return ReportOnReadSerializer
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        report = self.get_object()
        user = request.user
        status = request.data.get('status')
        comment_text = request.data.get('comment')

        if not request.user.is_staff:
            raise PermissionDenied('Только исполнители могут изменять статус жалобы!')
        
        if not comment_text:
            raise ValidationError('Перед обновлением статуса оставьте комментарий!')
        
        report.status = status
        report.save()
        
        Comments.objects.create(user=user, report=report, text=comment_text)
        serializer = ReportOnReadSerializer(report)
        return Response(serializer.data)


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