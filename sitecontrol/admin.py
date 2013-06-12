from sitecontrol.models import CoreSite, GitSource, NullSource, DeployCommand, QueuedUpdate, PageCheck, CoreHost
from django.contrib import admin
from django.db import models

def name_only(obj):
    return obj.name

class DeployCommandInline(admin.TabularInline):
    model = DeployCommand
    formfield_overrides = {
        models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width:90%;'})},
        models.TextField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width:50em;'})}
    }

class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'root', 'source']
    actions = ["queue_update"]
    inlines = [DeployCommandInline,]

    def queue_update(self, request, queryset):
        for site in queryset:
            if QueuedUpdate.objects.filter(site=site).count() == 0:
                QueuedUpdate(site=site).save()
                self.message_user(request, "%s was successfully placed in the queue." % site.name)
            else:
                self.message_user(request, "%s was already in the queue." % site.name)              
    queue_update.short_description = "Enqueue selected sites for update"

class PageCheckInline(admin.TabularInline):
    model = PageCheck

class HostAdmin(admin.ModelAdmin):
    list_display = ['host', 'site']
    inlines = [PageCheckInline,]

class NullSourceAdmin(admin.ModelAdmin):
    list_display = [name_only, 'reason', 'last_update', 'last_deploy']

class GitSourceAdmin(admin.ModelAdmin):
    list_display = [name_only, 'source_url', 'last_check', 'last_update', 'last_deploy']

admin.site.register(CoreSite, SiteAdmin)
admin.site.register(CoreHost, HostAdmin)
admin.site.register(GitSource, GitSourceAdmin)
admin.site.register(NullSource, NullSourceAdmin)

