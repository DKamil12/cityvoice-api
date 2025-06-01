from django.shortcuts import render
from django.db.models import Count, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from reports.models import Report, District
from django.utils.dateparse import parse_date
from rest_framework import status

from reports.models import Category
from surveys.models import SurveyResponse


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


class CitywideCategoryCorrelationView(APIView):
    def get(self, request):
        # Получаем все категории
        categories = Category.objects.all()

        result = []
        for cat in categories:
            # Средняя оценка по вопросам этой категории
            avg_rating = SurveyResponse.objects.filter(
                question__category=cat
            ).aggregate(avg=Avg("rating"))["avg"]

            # Кол-во жалоб в этой категории
            complaint_count = Report.objects.filter(
                category=cat
            ).count()

            result.append({
                "category_id": cat.id,
                "category_name": cat.name,
                "average_rating": round(avg_rating or 0, 2),
                "complaint_count": complaint_count,
            })

        return Response(result)


class DistrictCategoryCorrelationView(APIView):
    def get(self, request, district_id):
        try:
            district = District.objects.get(pk=district_id)
        except District.DoesNotExist:
            return Response({"detail": "District not found"}, status=status.HTTP_404_NOT_FOUND)

        categories = Category.objects.all()

        result = []
        for cat in categories:
            avg_rating = SurveyResponse.objects.filter(
                question__category=cat,
                district=district
            ).aggregate(avg=Avg("rating"))["avg"]

            complaint_count = Report.objects.filter(
                category=cat,
                district=district
            ).count()

            result.append({
                "category_id": cat.id,
                "category_name": cat.name,
                "average_rating": round(avg_rating or 0, 2),
                "complaint_count": complaint_count,
            })

        return Response(result)
