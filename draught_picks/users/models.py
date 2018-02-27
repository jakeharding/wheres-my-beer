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
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from parser.Grammar import DescriptionParser


class DraughtPicksUser(AbstractUser):
    REQUIRED_FIELDS = ['email', 'date_of_birth']
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date_of_birth = m.DateField()
    weight = m.IntegerField(help_text="Weight in pounds.", blank=True, null=True)
    favorite_beers = m.ManyToManyField('beers.Beer', related_name='favorite_beers')
    recent_beers = m.ManyToManyField('beers.Beer', related_name='recent_beers')
    rated_beers = m.ManyToManyField('beers.Beer', related_name='rated_beers', through='beers.BeerRating')


class BeerPreferences(m.Model):
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    abv_low = m.IntegerField(null=True, blank=True)
    abv_hi = m.IntegerField(null=True, blank=True)
    ibu_low = m.IntegerField(null=True, blank=True)
    ibu_hi = m.IntegerField(null=True, blank=True)
    like_description = m.TextField(null=True, blank=True)
    user = m.ForeignKey(DraughtPicksUser, related_name='beer_preferences', on_delete=m.PROTECT)
    created_at = m.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=BeerPreferences)
def parse_desc(sender, instance=None, **kwargs):
    p = DescriptionParser(instance.like_description)
    p.parse()
