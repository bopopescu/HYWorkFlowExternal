from django.db import models
from datetime import *
from administration.models import CompanyMaintenance

# Create your models here.
class AssetType(models.Model):
    class Meta:
        verbose_name_plural = 'AssetTypes'

    asset_type = models.CharField(max_length = 5)
    description = models.CharField(max_length = 100)
    status = models.BooleanField(default = True)
    created_by = models.CharField(max_length = 120)
    created_date = models.DateTimeField(auto_now_add = True)
    modify_by = models.CharField(max_length = 120)
    modify_date = models.DateTimeField(default = datetime.now, blank = True)
    is_deleted = models.BooleanField(default = False, null = True)
    delete_by = models.CharField(max_length = 120)
    delete_date = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.description


class AssetCategory(models.Model):
    class Meta:
        verbose_name_plural = 'AssetCategories'

    category_type = models.CharField(max_length = 5)
    description = models.CharField(max_length = 100)
    status = models.BooleanField(default = True)
    created_by = models.CharField(max_length = 120)
    created_date = models.DateTimeField(auto_now_add = True)
    modify_by = models.CharField(max_length = 120)
    modify_date = models.DateTimeField(default = datetime.now, blank = True)
    is_deleted = models.BooleanField(default = False, null = True)
    delete_by = models.CharField(max_length = 120)
    delete_date = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.description


class Tax(models.Model):
    class Meta:
        verbose_name_plural = 'Taxes'

    tax_code = models.CharField(max_length = 5)
    description = models.CharField(max_length = 100)
    status = models.BooleanField(default = True)
    created_by = models.CharField(max_length = 120)
    created_date = models.DateTimeField(auto_now_add = True)
    modify_by = models.CharField(max_length = 120)
    modify_date = models.DateTimeField(default = datetime.now, blank = True)
    is_deleted = models.BooleanField(default = False, null = True)
    delete_by = models.CharField(max_length = 120)
    delete_date = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.description


class ClassType(models.Model):
    class Meta:
        verbose_name_plural = 'ClassTypes'

    class_type = models.CharField(max_length = 5)
    description = models.CharField(max_length = 100)
    status = models.BooleanField(default = True)
    created_by = models.CharField(max_length = 120)
    created_date = models.DateTimeField(auto_now_add = True)
    modify_by = models.CharField(max_length = 120)
    modify_date = models.DateTimeField(default = datetime.now, blank = True)
    is_deleted = models.BooleanField(default = False, null = True)
    delete_by = models.CharField(max_length = 120)
    delete_date = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.description


class AssetMaster(models.Model):
    class Meta:
        verbose_name_plural = 'AssetsMaster'

    asset_number = models.CharField(max_length = 35)
    company = models.ForeignKey(CompanyMaintenance, verbose_name="Company", on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length = 150)
    asset_type_id = models.ForeignKey(AssetType, on_delete = models.CASCADE)
    asset_category_id = models.ForeignKey(AssetCategory, on_delete = models.CASCADE)
    tax_id = models.ForeignKey(Tax, on_delete = models.CASCADE)
    class_type_id = models.ForeignKey(ClassType, on_delete = models.CASCADE)
    acquisition_date = models.DateTimeField(default = datetime.now, null=True, blank=True)
    floor_plan_ref = models.CharField(max_length = 50)
    trustees = models.CharField(max_length = 50)
    cost_value = models.DecimalField(max_digits = 8, decimal_places = 2)
    net_book_value = models.DecimalField(max_digits = 8, decimal_places = 2)
    last_trn_date = models.DateField(default = datetime.now, null=True, blank=True)
    current_trn_date = models.DateField(default = datetime.now, null=True, blank=True)
    last_py_trn_date = models.DateField(default = datetime.now, null=True, blank=True)
    last_pm_trn_date = models.DateField(default = datetime.now, null=True, blank=True)
    disposal_date = models.DateField(default = datetime.now, null=True, blank=True)
    proceeds_on_disposal = models.DecimalField(max_digits = 8, decimal_places = 2)
    historical_cost = models.DecimalField(max_digits = 8, decimal_places = 2)
    active_lifetime = models.DecimalField(max_digits = 8, decimal_places = 2)
    active_res_value = models.DecimalField(max_digits = 8, decimal_places = 2)
    tax_cost = models.DecimalField(max_digits = 8, decimal_places = 2)
    current_tax_percentage = models.DecimalField(max_digits = 5, decimal_places = 2)
    status = models.BooleanField(default = True)
    remark = models.CharField(max_length = 300)
    created_by = models.CharField(max_length = 120,  null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add = True,  null=True, blank=True)
    modify_by = models.CharField(max_length = 120, null=True, blank=True)
    modify_date = models.DateTimeField(default = datetime.now, null=True, blank=True)
    is_deleted = models.BooleanField(default = False, null = True)
    delete_by = models.CharField(max_length = 120, null=True, blank=True)
    delete_date = models.DateTimeField(default = datetime.now, null=True, blank=True)

    def __str__(self):
        return self.description


class Statistics(models.Model):
    class Meta:
        verbose_name_plural = 'Statistics'

    asset_master_id = models.ForeignKey(AssetMaster, on_delete = models.CASCADE)
    elapsed_months_py = models.DecimalField(max_digits = 8, decimal_places = 2)
    elapsed_months_cy = models.DecimalField(max_digits = 8, decimal_places = 2)
    elapsed_months_pm = models.DecimalField(max_digits = 8, decimal_places = 2)
    ac_opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    additions = models.DecimalField(max_digits = 8, decimal_places = 2)
    revaluations = models.DecimalField(max_digits = 8, decimal_places = 2)
    disposals = models.DecimalField(max_digits = 8, decimal_places = 2)
    impairment = models.DecimalField(max_digits = 8, decimal_places = 2)
    ac_closing_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    ad_opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    depreciation_cost = models.DecimalField(max_digits = 8, decimal_places = 2)
    depreciation_revaluation = models.DecimalField(max_digits = 8, decimal_places = 2)
    depreciation_total = models.DecimalField(max_digits = 8, decimal_places = 2)
    acc_depr_revaluations = models.DecimalField(max_digits = 8, decimal_places = 2)
    acc_depr_disposals = models.DecimalField(max_digits = 8, decimal_places = 2)
    ad_closing_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    closing_carrying_value = models.DecimalField(max_digits = 8, decimal_places = 2)
    rr_opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    revaluation_surplus = models.DecimalField(max_digits = 8, decimal_places = 2)
    rr_depr_revaluation = models.DecimalField(max_digits = 8, decimal_places = 2)
    rr_closing_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    impairment_writeOffs = models.DecimalField(max_digits = 8, decimal_places = 2)
    profit_Loss_on_disposal = models.DecimalField(max_digits = 8, decimal_places = 2)
    cost = models.DecimalField(max_digits = 8, decimal_places = 2)
    revaluation = models.DecimalField(max_digits = 8, decimal_places = 2)
    total = models.DecimalField(max_digits = 8, decimal_places = 2)
    hc_opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    hc_ytd_movement = models.DecimalField(max_digits = 8, decimal_places = 2)
    hc_closing_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    hc_mtd_movement = models.DecimalField(max_digits = 8, decimal_places = 2)
    tv_opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    tv_ytd_movement = models.DecimalField(max_digits = 8, decimal_places = 2)
    tv_closing_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    tv_mtd_movement = models.DecimalField(max_digits = 8, decimal_places = 2)
    dt_opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    dt_ytd_movement = models.DecimalField(max_digits = 8, decimal_places = 2)
    dt_closing_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    dt_mtd_movement = models.DecimalField(max_digits = 8, decimal_places = 2)
    status = models.BooleanField(default = True)
    created_by = models.CharField(max_length = 120)
    created_date = models.DateTimeField(auto_now_add = True)
    modify_by = models.CharField(max_length = 120)
    modify_date = models.DateTimeField(default = datetime.now, blank = True)
    is_deleted = models.BooleanField(default = False, null = True)
    delete_by = models.CharField(max_length = 120)
    delete_date = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.asset_master_id
