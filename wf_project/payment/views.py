from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewPaymentForm,UpdatePaymentForm,DetailPaymentForm
from django.contrib.auth.decorators import login_required
from .models import PaymentRequest
from rest_framework import viewsets
from .serializers import PYSerializer

class PYViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all() #.order_by('rank')
    serializer_class = PYSerializer

@login_required
def py_create(request):    
    if request.method == 'POST':
        form = NewPaymentForm(request.POST)
        if form.is_valid():
            vendor = form.cleaned_data['vendor']
            currency = form.cleaned_data['currency']
            company = form.cleaned_data['company']
            transaction_type = form.cleaned_data['transaction_type']
            project = form.cleaned_data['project']
            payment_mode = form.cleaned_data['payment_mode']
            py = form.save(commit=False)
            py.vendor = vendor
            py.currency = currency
            py.company = company
            py.transaction_type = transaction_type
            py.project = project
            py.payment_mode = payment_mode
            py.save()
            return redirect(pylist)
        else:
            py = PaymentRequest
            form = NewPaymentForm()
    else:
        py = PaymentRequest
        form = NewPaymentForm()
    return render(request, 'pycreate.html', {'py': py, 'form': form})

@login_required
def py_delete(request, pk):
    py =  get_object_or_404(PaymentRequest, pk=pk)
    py.delete()
    return redirect(pylist)

@login_required
def py_detail(request, pk):
    py =  get_object_or_404(PaymentRequest, pk=pk)
    form = DetailPaymentForm(instance=py)
    return render(request, 'pydetail.html', {'py': py, 'form': form})

@login_required
def pylist(request):
    return render(request, 'pylist.html')

@login_required
def py_update(request, pk): 
    py = get_object_or_404(PaymentRequest, pk=pk)
    if request.method == 'POST':
        form = UpdatePaymentForm(request.POST, instance=py)
        if form.is_valid():
            py = form.save()
            py.revision = py.revision + 1
            py.save()
            return redirect('py_detail', pk=py.pk)
        else:
            print(form.errors)
    else:
        form = UpdatePaymentForm(instance=py)
    return render(request, 'pyupdate.html', {'py': py, 'form': form})