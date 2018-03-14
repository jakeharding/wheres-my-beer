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

from description_parser.Grammar import DescriptionParser
from beers.models import BeerLearning


class DraughtPicksUser(AbstractUser):

    MALE_CHOICE = 'M'
    FEMALE_CHOICE = 'F'
    OTHER_CHOICE = 'O'

    GENDER_CHOICES = (
        (MALE_CHOICE, 'Male'),
        (FEMALE_CHOICE, 'Female'),
        (OTHER_CHOICE, 'Other')
    )

    REQUIRED_FIELDS = ['email', 'date_of_birth']
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date_of_birth = m.DateField()
    weight = m.IntegerField(help_text="Weight in pounds.", blank=True, null=True)
    gender = m.CharField(max_length=1, choices=GENDER_CHOICES, default=FEMALE_CHOICE)
    favorite_beers = m.ManyToManyField('beers.Beer', related_name='favorite_beers')
    recent_beers = m.ManyToManyField('beers.Beer', related_name='recent_beers', through='beers.RecentBeer')
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
    beer_learning = m.OneToOneField('beers.BeerLearning', blank=True, null=True, on_delete=m.PROTECT)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=BeerPreferences)
def parse_desc(sender, instance=None, created=False, **kwargs):
    parsed = {}
    if instance.like_description:
        p = DescriptionParser(instance.like_description)
        parsed = p.parse()
    if not instance.beer_learning:
        instance.beer_learning = BeerLearning.objects.create(**parsed)
    else:
        # fields to update are in parsed.keys() and only set to 1
        # The difference between parsed.keys() and beer_learning.fields are set to zero
        zeros = instance.beer_learning.learning_fields - parsed.keys()
        for attr in zeros:
            setattr(instance.beer_learning, attr, 0)
        for k, v in parsed.items():
            setattr(instance.beer_learning, k, v)
        instance.beer_learning.save()
