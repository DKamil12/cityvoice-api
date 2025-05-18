from rest_framework import serializers
from .models import Category, Report, Comments, District
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializerOnRead(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Comments
        fields = '__all__'

class CommentSerializerOnWrite(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = ['user']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class ReportOnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['status', 'user', 'district']


class ReportOnReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    comments = CommentSerializerOnRead(many=True, read_only=True)
    district = DistrictSerializer()

    class Meta:
        model = Report
        fields = '__all__'


class ReportOnUpdateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = ['comment', 'status']
