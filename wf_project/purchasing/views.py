from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewPOForm
from .models import PurchaseOrder
from rest_framework import viewsets
from .serializers import POSerializer
from django.contrib.auth.models import User

class MyPOViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')
    serializer_class = POSerializer
    
    def get_queryset(self):
        return PurchaseOrder.objects.filter(submit_by=self.request.user.id)

class TeamPOViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-id')    
    serializer_class = POSerializer

    def get_queryset(self):
        groups = self.request.user.groups.values_list('id', flat=True)
        users = User.objects.filter(groups__in = groups).exclude(id=self.request.user.id).values_list('id', flat=True)
        return PurchaseOrder.objects.filter(submit_by__in=users)

@login_required
def po_delete(request, pk):
    po =  get_object_or_404(PurchaseOrder, pk=pk)
    po.delete()
    return redirect(po_list)

@login_required
def po_index(request):
    return redirect(po_list)

@login_required
def po_list(request):
    return render(request, 'po/list.html')

@login_required
def po_create(request):
    po = PurchaseOrder
    form = NewPOForm()
    return render(request, 'po/create.html', {'po': po, 'form': form})