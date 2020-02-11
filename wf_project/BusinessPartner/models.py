from django.db import models

class VendorQualification(models.Model):
    company = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    revision = models.IntegerField()
    docno = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    submitDate = models.DateTimeField()
