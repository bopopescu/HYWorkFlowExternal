from django.db import models
from payment.models import PaymentRequest
from administration.models import DrawerMaintenance
from django.contrib.auth.models import User

# Create your models here.
class DrawerDisbursement(models.Model):
    payment = models.ForeignKey(PaymentRequest, verbose_name="Payment Request", on_delete=models.CASCADE,  blank=True, null=True)
    status = models.CharField(max_length=1)
    total_disbursed = models.DecimalField(max_digits=10, decimal_places=2)
    disbursed_by = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null=True)
    disbursed_date = models.DateField(auto_now_add=True)
    drawer = models.ForeignKey(DrawerMaintenance, verbose_name="Drawer Maintenance", on_delete=models.CASCADE,  blank=True, null=True)