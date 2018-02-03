"""
models.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Models pertaining to users.
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models as m


class DraughtPicksUser(AbstractUser):
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date_of_birth = m.DateTimeField()
    weight = m.IntegerField(help_text="Weight in pounds.")


class BeerPreferences(m.Model):
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    abv_low = m.IntegerField(null=True, blank=True)
    abv_hi = m.IntegerField(null=True, blank=True)
    ibu_low = m.IntegerField(null=True, blank=True)
    ibu_hi = m.IntegerField(null=True, blank=True)
    like_description = m.TextField(null=True, blank=True)
    user = m.ForeignKey(DraughtPicksUser, related_name='beer_preferences')
