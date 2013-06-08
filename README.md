django-sitecontrol
========================

django-sitecontrol is a Django application to automatically or manually update other websites running on the same machine from a web interface.  Best used in conjunction with https://github.com/hach-que/Nginx-Secure.

Configuration
---------------

This Django app requires a bit of environment configuration in the main `settings.py` file.  Make sure that the `INSTALLED_APPS` contains at least the following (these are dependencies of django-sitecontrol).

```
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sitecontrol',
    'django.contrib.admin',
    'south',
    'ordered_model',
    'chronograph'
)
```

And add the respective URLs in `urls.py`:

```
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sitecontrol.views.index'),
    url(r'^ajax$', 'sitecontrol.views.ajax'),
    url(r'^update/(?P<id>[0-9]+)$', 'sitecontrol.views.update'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
```

You will also need to add the cron job so that chronograph can schedule updates by adding the following line to `/etc/crontab`:

```
* * * * * wwwusr-<siteuser> cd /srv/www/<site>/ && python /srv/www/<site>/manage.py cron
```

Setting Up
---------------

Once the application is running on a website, you need to add the Chronograph job to trigger `sitecontrol.syncsites` every minute.

You'll also need to set up the sudoers file so that the django-sitecontrol can change to the appropriate user for each site that it'll be updating.  Generally the sudoers rules should look like:

```
<deploy-site-user> ALL=(<target-site-user>) NOPASSWD: /bin/bash
```

Security
----------

For obvious reasons you should make sure this site is being served up over HTTPS, with appropriate web server level authentication in place (in addition to the authentication Django provides).
