"""
urls.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Constructs the urls for the REST API.
"""

from django.urls import re_path, include
from rest_framework.authtoken import views

urlpatterns = [
    re_path(r'^login', views.obtain_auth_token)
]