from django.db import models
from approval.models import ApprovalItem
from django.contrib.auth.models import User

class AccountTask(models.Model):
    approval_item = models.ForeignKey(ApprovalItem, on_delete=models.CASCADE, blank=True, null=True)
    process = models.BooleanField(default=False, blank=True, null=True)
    process_date = models.DateField(auto_now=True, blank=True, null=True)
    process_by = models.ForeignKey(User, related_name='processed_by_user', null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False, blank=True, null=True)
    completed_date = models.DateField(auto_now=True, blank=True, null=True)
    completed_by = models.ForeignKey(User, related_name='completed_by_user', null=True, blank=True, on_delete=models.SET_NULL)
