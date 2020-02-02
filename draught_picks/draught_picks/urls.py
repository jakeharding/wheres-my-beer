"""
urls.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Entry point to URL definition.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic.base import RedirectView

from users.views import EmailTemplateView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path(r'', RedirectView.as_view(url='/admin')),
    re_path(r'api/%s/' % settings.REST_API_VERSION, include('rest_api.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path('email/templates/(?P<name>.*)/', EmailTemplateView.as_view())
    ]
