from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewMemoForm
from .models import Memo
from administration.models import CompanyMaintenance, DepartmentMaintenance, ProjectMaintenance
from rest_framework import viewsets
from .serializers import MemoSerializer

def memo_list(request):
    return render(request, 'memo_list.html')

class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all() #.order_by('rank')
    serializer_class = MemoSerializer

def memo_create(request):    
    #company = get_object_or_404(CompanyMaintenance, co_pk)
    #department = get_object_or_404(DepartmentMaintenance, dept_pk)
    #project = get_object_or_404(ProjectMaintenance, proj_pk)
    #user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewMemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.company = company
            memo.department = department
            memo.project = project
            memo.save()
            return redirect('memo_list')  # TODO: redirect to the created topic page
    else:
        memo = Memo
        form = NewMemoForm()
    return render(request, 'memo_create.html', {'memo': memo, 'form': form})