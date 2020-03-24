from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewPOForm
from .models import PurchaseOrder
from rest_framework import viewsets
from .serializers import POSerializer

def po_list(request):
    return render(request, 'po_list.html')

class POViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all() #.order_by('rank')
    serializer_class = POSerializer

def po_create(request):
    po = PurchaseOrder
    form = NewPOForm()
    return render(request, 'po_create.html', {'po': po, 'form': form})