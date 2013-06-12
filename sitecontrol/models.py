from django.db import models
from django.core.exceptions import ValidationError
from ordered_model.models import OrderedModel
import pwd
import httplib
import subprocess
import sudo
from datetime import datetime
from django.utils.timezone import utc

def validate_unix_user(value):
    try:
        pw = pwd.getpwnam(value)
    except KeyError:
        raise ValidationError(u"%s is not a unix user on the local system!" % value)

class CoreSource(models.Model):
    name = models.CharField(max_length=200)
    last_update = models.DateTimeField(null=True)
    last_deploy = models.DateTimeField(null=True)

    def get_child(self):
        if hasattr(self, "nullsource"):
            return self.nullsource
        elif hasattr(self, "gitsource"):
            return self.gitsource
        else:
            raise Exception("Unknown source type")

    def requires_update(self, site):
        raise Exception("Use derived class to call `requires_update`.")

    def update(self, site):
        raise Exception("Use derived class to call `update`.")

    def __unicode__(self):
        return self.name + " (" + self.get_child().type + ")"

class CoreSite(models.Model):
    name = models.CharField(max_length=200)
    root = models.CharField(max_length=200)
    user = models.CharField(max_length=200, validators=[validate_unix_user])
    source = models.ForeignKey(CoreSource)
    updating = models.BooleanField()

    def __unicode__(self):
        return self.name

    def get_source(self):
        return self.source.get_child()

class CoreHost(models.Model):
    site = models.ForeignKey(CoreSite)
    host = models.CharField(max_length=200)

    def get_status(self):
        for check in PageCheck.objects.filter(host=self):
            conn = httplib.HTTPConnection(self.host, timeout=0.5)
            conn.request("GET", check.path)
            try:
                resp = conn.getresponse()
                if resp.status >= 400 and \
                   resp.status < 500:
                    return "damaged"
                if resp.status >= 500:
                    return "offline"
            except Exception:
                return "offline"
        return "healthy"

class PageCheck(models.Model):
    host = models.ForeignKey(CoreHost)
    path = models.CharField(max_length=500)

class GitSource(CoreSource):
    source_url = models.CharField(max_length=500)
    poll_period_minutes = models.PositiveSmallIntegerField()
    last_check = models.DateTimeField(auto_now_add=True)
    type = "Git Source"
 
    def __unicode__(self):
        return self.name
   
    def run_command(self, user, args, working_directory):
        process = sudo.run(user, " ".join(args), working_directory)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            return None
        return stdout

    def requires_update(self, site):
        if (datetime.utcnow().replace(tzinfo=utc) - self.last_check).total_seconds() < self.poll_period_minutes * 60:
            return False
        self.last_check = datetime.utcnow().replace(tzinfo=utc)
        self.save()
        if self.source_url == None or self.source_url.strip() == "":
            return False
        if self.run_command(site.user, ["git", "remote", "set-url", "origin", self.source_url], site.root) == None:
            return False
        if self.run_command(site.user, ["git", "fetch"], site.root) == None:
            return False
        current = self.run_command(site.user, ["git", "symbolic-ref", "-q", "HEAD"], site.root)
        if current == None or current.strip() == "":
            return False
        upstream = self.run_command(site.user, ["git", "for-each-ref", "--format='%(upstream:short)'", current], site.root)
        if upstream == None or upstream.strip() == "":
            return False
        incoming = self.run_command(site.user, ["git", "rev-list", ".."+upstream], site.root)
        if incoming == None or incoming.strip() == "":
            return False
        return True

    def update(self, site):
        self.run_command(site.user, ["git", "pull"], site.root)
        self.last_update = datetime.utcnow().replace(tzinfo=utc)
        self.save()
        return True

class NullSource(CoreSource):
    reason = models.TextField()
    type = "Null Source"

    def __unicode__(self):
        return self.name

    def requires_update(self, site):
        return False

    def update(self, site):
        self.last_update = datetime.utcnow().replace(tzinfo=utc)
        self.save()
        pass

class DeployCommand(OrderedModel):
    site = models.ForeignKey(CoreSite)
    program = models.CharField(max_length=200)
    arguments = models.TextField()

    def __unicode__(self):
        return self.program + " " + self.arguments

class QueuedUpdate(models.Model):
    site = models.ForeignKey(CoreSite)

