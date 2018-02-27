"""
models.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Models pertaining to beers.
"""
import uuid

from django.db import models as m
from django.conf import settings


class Beer(m.Model):
    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=255)
    description = m.TextField(blank=True, null=True)
    abv = m.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    ibu = m.PositiveSmallIntegerField(blank=True, null=True)
    api_id = m.CharField(max_length=255, help_text="Unique id of the api the beer was pulled from")
    name_of_api = m.CharField(max_length=255, help_text="Name of the api used to get data.")
    created_at = m.DateTimeField(auto_now_add=True, help_text="Date and time the beer was added to this database")

    def __str__(self):
        return self.name


class BeerRating(m.Model):
    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.PROTECT)
    beer = m.ForeignKey(Beer, on_delete=m.PROTECT)
    rating = m.PositiveSmallIntegerField()
    description = m.TextField(blank=True, null=True)
    created_at = m.DateTimeField(auto_now_add=True)


class RecentBeer(m.Model):
    uuid = m.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.PROTECT)
    beer = m.ForeignKey(Beer, on_delete=m.PROTECT)
    created_at = m.DateTimeField(auto_now_add=True)
