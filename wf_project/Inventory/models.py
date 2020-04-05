from django.db import models
from administration.models import ItemClassesMaintenance
from administration.models import ItemGroupsMaintenance
from administration.models import UOMMaintenance
from django.contrib.auth.models import User

class Item(models.Model):
    item_type = models.CharField(max_length=100)
    item_class = models.ForeignKey(ItemClassesMaintenance, verbose_name="Item Class",null=True, blank=True, on_delete=models.CASCADE)
    item_group = models.ForeignKey(ItemGroupsMaintenance, verbose_name="Item Group",null=True, blank=True, on_delete=models.CASCADE)
    item_code = models.CharField(max_length=100)
    item_description = models.CharField(max_length=250)
    item_category = models.ForeignKey('ItemCategoryMaintenance',related_name="item_category" ,on_delete=models.CASCADE)
    item_subcategory = models.ForeignKey('ItemCategoryMaintenance',related_name="item_subcategory",null=True, blank=True, on_delete=models.CASCADE)
    item_subsubcategory = models.ForeignKey('ItemCategoryMaintenance',related_name="item_subsubcategory",null=True, blank=True, on_delete=models.CASCADE)
    item_uom = models.ForeignKey(UOMMaintenance,on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    specification = models.CharField(max_length=100)
    hs_code = models.CharField(max_length=100)
    minimum_quantity = models.IntegerField()
    minimum_order_quantity = models.IntegerField()
    standard_packing_quantity = models.IntegerField()
    leadtime = models.IntegerField()
    remarks = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='itemcreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='itemmodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item Master Data'
        verbose_name_plural = 'Item Master Data'

    def __str__(self):
        return self.item_code + ' - ' + self.item_description

class ItemCategoryMaintenance(models.Model):
    category_name = models.CharField(max_length=250)
    is_active = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='itemcategorycreated_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='itemcategorymodified_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    modified_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name