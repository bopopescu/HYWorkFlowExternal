from django.contrib import admin
from .models import VendorQualification
from .models import VendorEvaluation

admin.site.register(VendorQualification)
admin.site.register(VendorEvaluation)