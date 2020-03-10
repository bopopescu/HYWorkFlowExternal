from django.db import models
from administration.models import CurrencyMaintenance

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    currency = models.ForeignKey(CurrencyMaintenance, default=0, verbose_name="Currency",on_delete=models.CASCADE)
    business_registration_no = models.CharField(max_length=30)
    tax_id_1 = models.CharField(max_length=100)
    tax_id_2 = models.CharField(max_length=100)
    is_company = models.BooleanField()
    created_by = models.CharField(max_length=100,editable=False)
    created_timestamp = models.DateField(editable=False)
    modified_by = models.CharField(max_length=100,editable=False)
    modified_timestamp = models.DateField(editable=False)
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.customer_name