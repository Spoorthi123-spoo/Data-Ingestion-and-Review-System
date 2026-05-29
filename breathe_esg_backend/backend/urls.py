from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from esg_ingestion import views


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

    # -----------------------------------
    # ESG INGESTION
    # -----------------------------------
    path('api/upload/', views.upload_data),
    path('api/records/', views.get_records),

    # -----------------------------------
    # REVIEW SYSTEM
    # -----------------------------------
    path('api/pending/', views.pending_records),
    path('api/approve/<int:record_id>/', views.approve_record),
    path('api/reject/<int:record_id>/', views.reject_record),

    # -----------------------------------
    # AUDIT SYSTEM
    # -----------------------------------
    path('api/audit/', views.audit_logs),

    # -----------------------------------
    # DASHBOARD (🔥 NEW IMPORTANT ADDITION)
    # -----------------------------------
    path('api/dashboard/', views.dashboard),
]