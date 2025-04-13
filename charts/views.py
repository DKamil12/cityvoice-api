from django.shortcuts import render
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from reports.models import Report
from django.utils.dateparse import parse_date

# Create your views here.
class ReportsByCategoryView(APIView):
    def get(self, request, format=None):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        reports = Report.objects.all()

        if start_date:
            reports = reports.filter(created_at__gte=parse_date(start_date))
        if end_date:
            reports = reports.filter(created_at__lte=parse_date(end_date))

        data = (
            reports.values('category__name').annotate(total=Count('id')).order_by('-total')
        )

        return Response(data)
    