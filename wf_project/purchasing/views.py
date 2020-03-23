from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewPOForm
from .models import PurchaseOrder
from rest_framework import viewsets
from .serializers import POSerializer

def polist(request):
    return render(request, 'polist.html')

class POViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all() #.order_by('rank')
    serializer_class = POSerializer

def pocreate(request):
    po = PurchaseOrder
    form = NewPOForm()
    return render(request, 'pocreate.html', {'po': po, 'form': form})