from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewMemoForm, DetailMemoForm, UpdateMemoForm
from django.contrib.auth.decorators import login_required
from .models import Memo
from administration.models import CompanyMaintenance, DepartmentMaintenance, ProjectMaintenance, MemoTemplateMaintenance
from rest_framework import viewsets
from .serializers import MemoSerializer

class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all() #.order_by('rank')
    serializer_class = MemoSerializer

@login_required
def memo_create(request):    
    if request.method == 'POST':
        form = NewMemoForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            department = form.cleaned_data['department']
            project = form.cleaned_data['project']
            template = form.cleaned_data['template']
            memo = form.save(commit=False)
            memo.company = company
            memo.department = department
            memo.project = project
            memo.template = template
            memo.save()
            return redirect(memo_list)
    else:
        memo = Memo
        form = NewMemoForm()
    return render(request, 'create.html', {'memo': memo, 'form': form})

@login_required
def memo_delete(request, pk):
    memo =  get_object_or_404(Memo, pk=pk)
    memo.delete()
    return redirect(memo_list)

@login_required
def memo_detail(request, pk):
    memo =  get_object_or_404(Memo, pk=pk)
    form = DetailMemoForm(instance=memo)
    return render(request, 'detail.html', {'memo': memo, 'form': form})

@login_required
def memo_list(request):
    return render(request, 'list.html')

@login_required
def memo_update(request, pk): 
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        form = UpdateMemoForm(request.POST, instance=memo)
        if form.is_valid():
            memo = form.save()
            memo.revision = memo.revision + 1
            memo.save()
            return redirect('memo_detail', pk=memo.pk)
        else:
            print(form.errors)
    else:
        form = UpdateMemoForm(instance=memo)
    return render(request, 'update.html', {'memo': memo, 'form': form})
    
        
    