from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .serializers import AssetMasterSerializer
from rest_framework import viewsets
from django.http import JsonResponse
import datetime

class MyAssetViewSet(viewsets.ModelViewSet):
    queryset = AssetMaster.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = AssetMasterSerializer

@login_required
def fixed_asset_list(request):
    return render(request, 'fixed_asset/list.html')

@login_required
def fixed_asset_create(request):
    if request.method == 'POST':
        form = AssetMasterForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.remark = request.POST['remark']
            asset.save()
            return redirect(fixed_asset_detail, asset.pk)
    else:
        form = AssetMasterForm()
    return render(request, 'fixed_asset/create_update.html', {'form': form})

@login_required
def fixed_asset_update(request, pk):
    asset = get_object_or_404(AssetMaster, pk=pk)
    if request.method == 'POST':
        form = AssetMasterForm(request.POST, instance=asset)
        asset.modify_by = request.user.username
        if form.is_valid():
            asset = form.save(commit=False)
            asset.remark = request.POST['remark']
            asset.save()
            return redirect(fixed_asset_detail, asset.pk)
    else:
        form = AssetMasterForm(instance=asset)
        form.fields['remark'].initial = asset.remark
        form.fields['company'].initial = asset.company
    return render(request, 'fixed_asset/create_update.html', {'form': form, 'asset': asset})

@login_required
def fixed_asset_delete(request):
    asset = get_object_or_404(AssetMaster, pk=request.POST['hiddenValue'])
    asset.is_deleted = True
    asset.delete_by=request.user.username
    asset.delete_date=datetime.now
    asset.save()
    return JsonResponse({'message': 'Success'})

@login_required
def fixed_asset_detail(request, pk):
    asset = get_object_or_404(AssetMaster, pk=pk)
    form = AssetMasterForm(instance=asset)
    form.fields['remark'].initial = asset.remark
    form.fields['company'].initial = asset.company
    return render(request, 'fixed_asset/detail.html', {'form': form, 'asset': asset})
