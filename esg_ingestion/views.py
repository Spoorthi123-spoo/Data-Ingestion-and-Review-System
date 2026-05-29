import pandas as pd

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

# -----------------------------------
# MODELS
# -----------------------------------
from .models import (
    Company,
    DataSource,
    RawRecord,
    NormalizedRecord,
    AuditTrail
)

# -----------------------------------
# NORMALIZATION ENGINE
# -----------------------------------
from normalization.engine import normalize_record


# -----------------------------------
# HOME API
# -----------------------------------
def home(request):
    return JsonResponse({
        "message": "Breathe ESG Backend Running Successfully"
    })


# -----------------------------------
# DASHBOARD API
# -----------------------------------
def dashboard(request):

    total_records = NormalizedRecord.objects.count()

    pending = NormalizedRecord.objects.filter(review_status="PENDING").count()
    approved = NormalizedRecord.objects.filter(review_status="APPROVED").count()
    rejected = NormalizedRecord.objects.filter(review_status="REJECTED").count()

    suspicious = NormalizedRecord.objects.filter(suspicious=True).count()

    total_emissions = NormalizedRecord.objects.aggregate(
        total=Sum("emissions_kg_co2e")
    )["total"] or 0

    return JsonResponse({
        "total_records": total_records,
        "pending_records": pending,
        "approved_records": approved,
        "rejected_records": rejected,
        "suspicious_records": suspicious,
        "total_emissions_kg_co2e": total_emissions
    })


# -----------------------------------
# GET ALL RECORDS
# -----------------------------------
def get_records(request):
    records = list(NormalizedRecord.objects.all().values())
    return JsonResponse(records, safe=False)


# -----------------------------------
# GET PENDING RECORDS
# -----------------------------------
def pending_records(request):
    records = list(NormalizedRecord.objects.filter(review_status="PENDING").values())
    return JsonResponse(records, safe=False)


# -----------------------------------
# APPROVE RECORD
# -----------------------------------
@csrf_exempt
def approve_record(request, record_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        record = NormalizedRecord.objects.get(id=record_id)
    except NormalizedRecord.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)

    old_status = record.review_status
    record.review_status = "APPROVED"
    record.save()

    AuditTrail.objects.create(
        record=record,
        action="APPROVED",
        performed_by="admin",
        previous_status=old_status,
        new_status="APPROVED"
    )

    return JsonResponse({"message": "Record approved"})


# -----------------------------------
# REJECT RECORD
# -----------------------------------
@csrf_exempt
def reject_record(request, record_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        record = NormalizedRecord.objects.get(id=record_id)
    except NormalizedRecord.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)

    old_status = record.review_status
    record.review_status = "REJECTED"
    record.save()

    AuditTrail.objects.create(
        record=record,
        action="REJECTED",
        performed_by="admin",
        previous_status=old_status,
        new_status="REJECTED"
    )

    return JsonResponse({"message": "Record rejected"})


# -----------------------------------
# UPLOAD + INGESTION API (FINAL ADVANCED)
# -----------------------------------
@csrf_exempt
def upload_data(request):

    if request.method != 'POST':
        return JsonResponse({"error": "POST request required"}, status=400)

    file = request.FILES.get('file')
    source_type = request.POST.get('source_type')

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    if not source_type:
        return JsonResponse({"error": "source_type is required"}, status=400)

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return JsonResponse({"error": f"Invalid CSV file: {str(e)}"}, status=400)

    company, _ = Company.objects.get_or_create(name="Demo Company")

    datasource = DataSource.objects.create(
        company=company,
        source_type=source_type,
        uploaded_file=file
    )

    inserted = 0
    source_type_clean = source_type.upper()

    # -----------------------------------
    # PROCESS EACH ROW
    # -----------------------------------
    for _, row in df.iterrows():

        raw_record = RawRecord.objects.create(
            source=datasource,
            raw_json=row.to_dict(),
            ingestion_status="SUCCESS"
        )

        # -----------------------------------
        # SAFE NORMALIZATION CALL
        # -----------------------------------
        try:
            norm = normalize_record(row, source_type_clean)
        except Exception as e:
            norm = {
                "activity_value": 0,
                "emissions_kg_co2e": 0,
                "suspicious": True
            }

        # -----------------------------------
        # CREATE NORMALIZED RECORD
        # -----------------------------------
        record = NormalizedRecord.objects.create(
            company=company,
            category=source_type_clean,
            activity_value=norm["activity_value"],
            unit="STANDARD_UNIT",
            emissions_kg_co2e=norm["emissions_kg_co2e"],
            suspicious=norm["suspicious"],
            source_record=raw_record
        )

        AuditTrail.objects.create(
            record=record,
            action="UPDATED",
            performed_by="system",
            previous_status="N/A",
            new_status="PENDING"
        )

        inserted += 1

    return JsonResponse({
        "message": "Upload successful",
        "rows_inserted": inserted
    })


# -----------------------------------
# AUDIT LOGS
# -----------------------------------
def audit_logs(request):
    logs = list(AuditTrail.objects.all().values())
    return JsonResponse(logs, safe=False)