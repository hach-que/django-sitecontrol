from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from sitecontrol.models import CoreSite, CoreHost, QueuedUpdate
from chronograph.models import Job

def update(request, id):
    if not request.user.is_authenticated() and not request.user.is_superuser:
        return redirect("/admin")
    site = CoreSite.objects.get(pk=id)
    if QueuedUpdate.objects.filter(site=site).count() == 0:
        QueuedUpdate(site=site).save()
    return redirect("/")

def _base(request):
    sites = []
    for site_model in CoreSite.objects.all():
        site = {
            "id": site_model.id,
            "name": site_model.name,
            "hosts": [],
            "is_queued": (QueuedUpdate.objects.filter(site=site_model).count() > 0),
            "is_updating": site_model.updating
        }
        for host_model in CoreHost.objects.filter(site=site_model):
            site["hosts"].append({
                "host": host_model.host,
                "status": host_model.get_status()
            })
        sites.append(site)
    return {
        "next_update": Job.objects.get(name="Sync and Update Websites").get_timeuntil().translate("en"),
        'sites': sites
    }

def index(request):
    if not request.user.is_authenticated() and not request.user.is_superuser:
        return redirect("/admin")
    return render(request, 'index.htm', _base(request))

def ajax(request):
    if not request.user.is_authenticated() and not request.user.is_superuser:
        return redirect("/admin")
    return render(request, 'content.htm', _base(request))
