from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewStaffRecruimentForm,UpdateStaffRecruimentForm,DetailStaffRecruimentForm
from django.contrib.auth.decorators import login_required
from .models import StaffRecruitmentRequest
from rest_framework import viewsets
from .serializers import StaffRecruitmentSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = StaffRecruitmentRequest.objects.all() #.order_by('rank')
    serializer_class = StaffRecruitmentSerializer

@login_required
def staff_create(request):    
    if request.method == 'POST':
        form = NewStaffRecruimentForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            reporting_to = form.cleaned_data['reporting_to']
            department = form.cleaned_data['department']
            position_title = form.cleaned_data['position_title']
            hire_type = form.cleaned_data['hire_type']
            staff = form.save(commit=False)
            staff.reporting_to = reporting_to
            staff.department = department
            staff.company = company
            staff.position_title = position_title
            staff.hire_type = hire_type
            staff.save()
            return redirect(staff_list)
        else:
            staff = StaffRecruitmentRequest
            form = NewStaffRecruimentForm()
    else:
        staff = StaffRecruitmentRequest
        form = NewStaffRecruimentForm()
    return render(request, 'staffrecruitmentcreate.html', {'staff': staff, 'form': form})

@login_required
def staff_delete(request, pk):
    staff =  get_object_or_404(StaffRecruitmentRequest, pk=pk)
    staff.delete()
    return redirect(staff_list)

@login_required
def staff_detail(request, pk):
    staff =  get_object_or_404(StaffRecruitmentRequest, pk=pk)
    form = DetailStaffRecruimentForm(instance=staff)
    return render(request, 'staffrecruitmentdetail.html', {'staff': staff, 'form': form})

@login_required
def staff_list(request):
    return render(request, 'staffrecruitmentlist.html')

@login_required
def staff_update(request, pk): 
    staff = get_object_or_404(StaffRecruitmentRequest, pk=pk)
    if request.method == 'POST':
        form = UpdateStaffRecruimentForm(request.POST, instance=staff)
        if form.is_valid():
            staff = form.save()
            staff.revision = staff.revision + 1
            staff.save()
            return redirect('staff_detail', pk=staff.pk)
        else:
            print(form.errors)
    else:
        form = UpdateStaffRecruimentForm(instance=staff)
    return render(request, 'staffrecruitmentupdate.html', {'staff': staff, 'form': form})