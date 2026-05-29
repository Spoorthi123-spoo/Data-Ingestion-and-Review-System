from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from esg_ingestion import views

# -----------------------------------
# JWT IMPORT (ADD THIS)
# -----------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# -----------------------------------
# HOME API
# -----------------------------------
def home(request):
    return JsonResponse({
        "message": "Breathe ESG Backend Running Successfully"
    })


urlpatterns = [
    path('admin/', admin.site.urls),

    # HOME
    path('', home),

    # ESG APIs
    path('api/upload/', views.upload_data),
    path('api/records/', views.get_records),

    # REVIEW SYSTEM
    path('api/pending/', views.pending_records),
    path('api/approve/<int:record_id>/', views.approve_record),
    path('api/reject/<int:record_id>/', views.reject_record),

    # AUDIT
    path('api/audit/', views.audit_logs),

    # -----------------------------------
    # JWT AUTH (ADD THIS SECTION)
    # -----------------------------------
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]