from django.core.management.base import BaseCommand, CommandError
from sitecontrol.models import QueuedUpdate, CoreSite, DeployCommand
from sitecontrol import sudo
import subprocess
import sys
import traceback
from datetime import datetime
from django.utils.timezone import utc

class Command(BaseCommand):
    args = ''
    help = 'Synchronises and updates websites.'

    def handle(self, *args, **options):
        to_update = []
        for item in QueuedUpdate.objects.all():
            to_update.append(item.site)
            item.delete()
        for site in CoreSite.objects.all():
            if site.get_source().requires_update(site):
                exists = False
                for i in to_update:
                    if i.name == site.name:
                        exists = True
                        break
                if not exists:
                    to_update.append(site)

        for site in to_update:
            site.updating = True
            site.save()
            try:
                print "~ Updating source for '" + site.name + "'..."
                site.get_source().update(site)
                print "~ Performing deployment for '" + site.name + "'..."
                self.do_deploy(site)
                
                src = site.get_source()
                src.last_deploy = datetime.utcnow().replace(tzinfo=utc)
                src.save()
                
            except Exception, ex:
                traceback.print_exc()
            site.updating = False
            site.save()

    def do_deploy(self, site):
        for command in DeployCommand.objects.filter(site=site):
            print "+ " + command.program + " " + command.arguments
            p = sudo.run(site.user, command.program + " " + command.arguments, site.root)
            out, err = p.communicate()
            sys.stdout.write(out)
            sys.stderr.write(err)
        
