from django.shortcuts import render
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from reports.models import Report, District
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
    

class ReportsByDistrictView(APIView):
    def get(self, request, format=None):
        start_date = request.GET.get('start_date')
        end_date   = request.GET.get('end_date')

        qs = Report.objects.all()
        if start_date:
            qs = qs.filter(created_at__gte=parse_date(start_date))
        if end_date:
            qs = qs.filter(created_at__lte=parse_date(end_date))

        data = (
            qs
            .values('district__name')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        # результат: [{"district__name": "Медеуский", "total": 29}, ...]
        return Response(data)
    

class DistrictCategoryStatsView(APIView):
    """
    GET /reports/districts/{district_id}/stats/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD

    Ответ:
    {
      "district_id": 5,
      "district_name": "Бостандыкский",
      "total": 94,
      "categories": [
        {"name": "Мусор", "count": 28},
        {"name": "Повреждения дорожного покрытия", "count": 12},
        …
      ]
    }
    """
    def get(self, request, district_id, format=None):
        # попытаемся найти район
        try:
            district = District.objects.get(pk=district_id)
        except District.DoesNotExist:
            return Response({"detail": "District not found"}, status=404)

        # базовый queryset по району
        qs = Report.objects.filter(district=district)

        # фильтры по дате
        start = request.GET.get("start_date")
        end   = request.GET.get("end_date")
        if start:
            qs = qs.filter(created_at__date__gte=parse_date(start))
        if end:
            qs = qs.filter(created_at__date__lte=parse_date(end))

        # общее число жалоб
        total = qs.count()

        # разбивка по категориям
        raw = (
            qs
            .values("category__id", "category__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        categories = [
            {"id": item["category__id"], "name": item["category__name"], "count": item["count"]}
            for item in raw
        ]

        return Response({
            "district_id": district.id,
            "district_name": district.name,
            "total": total,
            "categories": categories
        })