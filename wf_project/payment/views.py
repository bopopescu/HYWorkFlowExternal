from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewPaymentForm
from .models import PaymentRequest
from rest_framework import viewsets
from .serializers import PYSerializer

def pylist(request):
    return render(request, 'pylist.html')

class PYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all() #.order_by('rank')
    serializer_class = PYSerializer

def pycreate(request):
    py = PaymentRequest
    form = NewPaymentForm()
    return render(request, 'pycreate.html', {'py': py, 'form': form})