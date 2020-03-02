from django.db import models
from administration.models import ItemClassesMaintenance
from administration.models import ItemGroupsMaintenance

class Item(models.Model):
    item_type = models.CharField(max_length=1)
    prefix = models.CharField(max_length=100)
    item_class = models.ForeignKey(ItemClassesMaintenance, verbose_name="Item Class", on_delete=models.CASCADE)
    item_group = models.ForeignKey(ItemGroupsMaintenance, verbose_name="Item Group", on_delete=models.CASCADE)
    item_code = models.CharField(max_length=100)
    item_description = models.CharField(max_length=250)
    origin = models.CharField(max_length=100)
    specification = models.CharField(max_length=100)
    hs_code = models.CharField(max_length=100)
    minimum_quantity = models.IntegerField()
    minimum_order_quantity = models.IntegerField()
    standard_packing_quantity = models.IntegerField()
    leadtime = models.IntegerField()
    remarks = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_timestamp = models.DateField()
    modified_by = models.CharField(max_length=100)
    modified_timestamp = models.DateField()

    def __str__(self):
        return self.item_code