from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
from rest_framework import viewsets
from administration.models import TransactiontypeMaintenance
from approval.models import ApprovalItem
from .models import AccountTask
from .serializers import TaskSerializer
import datetime

class UnprocessedViewSet(viewsets.ModelViewSet):
    queryset = AccountTask.objects.all().order_by('-id')
    serializer_class = TaskSerializer

    def get_queryset(self):
        return AccountTask.objects.filter(process=False, completed=False).annotate(row_number=Window(expression=RowNumber(), order_by=F('id').desc())).order_by('-id')

class ProcessedViewSet(viewsets.ModelViewSet):
    queryset = AccountTask.objects.all().order_by('-id')
    serializer_class = TaskSerializer

    def get_queryset(self):
        return AccountTask.objects.filter(process=True, completed=False).annotate(row_number=Window(expression=RowNumber(), order_by=F('id').desc())).order_by('-id')

class CompletedViewSet(viewsets.ModelViewSet):
    queryset = AccountTask.objects.all().order_by('-id')
    serializer_class = TaskSerializer

    def get_queryset(self):
        return AccountTask.objects.filter(process=True, completed=True).annotate(row_number=Window(expression=RowNumber(), order_by=F('id').desc())).order_by('-id')

@login_required
def task_init(request):
    """Initializa task"""

    transaction_types = TransactiontypeMaintenance.objects.filter(send_to_account=True).values_list('id', flat=True)
    workflow_exist = AccountTask.objects.all().values_list('approval_item_id', flat=True)
    approval_list = ApprovalItem.objects.filter(status="A", transaction_type__in=transaction_types).exclude(pk__in=workflow_exist)

    for approval_item in approval_list:
        AccountTask.objects.create(approval_item=approval_item)

@login_required
def task_list(request):
    """Handles a list of task"""
    
    task_init(request)

    unprocessed = AccountTask.objects.filter(process=False, completed=False).count()
    processed = AccountTask.objects.filter(process=True, completed=False).count()
    completed = AccountTask.objects.filter(process=True, completed=True).count()

    return render(request, 'accounts_task/list.html', {'unprocessed': unprocessed, 'processed': processed, 'completed': completed})

@login_required
def task_process_all(request, pk):
    task = get_object_or_404(AccountTask, pk=pk)
    task.process = True
    task.process_date = datetime.datetime.today
    task.process_by = request.user
    task.save()

    return JsonResponse({'message': 'Success'})

@login_required
def task_complete_all(request, pk):
    task = get_object_or_404(AccountTask, pk=pk)
    task.completed = True
    task.completed_date = datetime.datetime.today
    task.completed_by = request.user
    task.save()

    return JsonResponse({'message': 'Success'})
    