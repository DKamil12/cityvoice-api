from django.contrib import admin
from django.urls import path, include
from .views import CustomTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static
from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('reports.urls')),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/token/', CustomTokenObtainPairView.as_view()),
    path('api/v1/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/charts/', include('charts.urls')),
    path('api/v1/statistics/survey/', include('surveys.urls')),
    path('api/v1/rewards/', include('rewards.urls')),
]
# if not DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
