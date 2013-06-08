from django.db import models
from django.core.exceptions import ValidationError
from ordered_model.models import OrderedModel
import pwd
import httplib

def validate_unix_user(value):
    try:
        pw = pwd.getpwnam(value)
    except KeyError:
        raise ValidationError(u"%s is not a unix user on the local system!" % value)

class CoreSource(models.Model):
    name = models.CharField(max_length=200)

    def get_child(self):
        if hasattr(self, "nullsource"):
            return NullSource(self.nullsource)
        elif hasattr(self, "gitsource"):
            return GitSource(self.gitsource)
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
    type = "Git Source"

    def requires_update(self, site):
        raise Exception("Not implemented.")

    def update(self, site):
        raise Exception("Not implemented.")

class NullSource(CoreSource):
    reason = models.TextField()
    type = "Null Source"

    def requires_update(self, site):
        return False

    def update(self, site):
        pass

class DeployCommand(OrderedModel):
    site = models.ForeignKey(CoreSite)
    program = models.CharField(max_length=200)
    arguments = models.TextField()

    def __unicode__(self):
        return self.program + " " + self.arguments

class QueuedUpdate(models.Model):
    site = models.ForeignKey(CoreSite)

