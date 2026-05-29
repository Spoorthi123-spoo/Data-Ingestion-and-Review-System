from django.db import models


# -----------------------------------
# COMPANY
# -----------------------------------
class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# -----------------------------------
# DATA SOURCE
# -----------------------------------
class DataSource(models.Model):

    SOURCE_TYPES = [
        ("SAP", "SAP"),
        ("UTILITY", "UTILITY"),
        ("TRAVEL", "TRAVEL"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPES
    )

    uploaded_file = models.FileField(upload_to='uploads/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.source_type}"


# -----------------------------------
# RAW DATA (UNCHANGED INPUT)
# -----------------------------------
class RawRecord(models.Model):

    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)

    raw_json = models.JSONField()

    ingestion_status = models.CharField(
        max_length=50,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)


# -----------------------------------
# NORMALIZED DATA (CLEANED ESG DATA)
# -----------------------------------
class NormalizedRecord(models.Model):

    REVIEW_STATUS = [
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    category = models.CharField(max_length=100)

    activity_value = models.FloatField()

    unit = models.CharField(max_length=20)

    emissions_kg_co2e = models.FloatField(null=True, blank=True)

    suspicious = models.BooleanField(default=False)

    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS,
        default="PENDING"
    )

    source_record = models.ForeignKey(
        RawRecord,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.activity_value}"


# -----------------------------------
# AUDIT TRAIL (IMPORTANT FOR INTERVIEW)
# -----------------------------------
class AuditTrail(models.Model):

    ACTION_TYPES = [
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
        ("UPDATED", "UPDATED"),
    ]

    record = models.ForeignKey(NormalizedRecord, on_delete=models.CASCADE)

    action = models.CharField(
        max_length=50,
        choices=ACTION_TYPES
    )

    performed_by = models.CharField(max_length=255)

    previous_status = models.CharField(max_length=20, null=True, blank=True)

    new_status = models.CharField(max_length=20, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record.id} - {self.action}"