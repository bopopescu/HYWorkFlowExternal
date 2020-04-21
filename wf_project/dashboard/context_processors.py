from django.shortcuts import get_object_or_404
from administration.models import DrawerMaintenance, DrawerUserMaintenance

def dashboard_drawer(request):
    if request.user.id != None:
        drawer_user = DrawerUserMaintenance.objects.filter(user=request.user).values_list('drawer_id', flat=True)

        return {
            'dashboard_drawer': DrawerMaintenance.objects.filter(drawer_status='O',id__in=drawer_user).order_by('drawer_name')
        }
    else:
        return ""


