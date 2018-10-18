"""
models.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Models pertaining to users.
"""
import uuid
#import tensorflow as tf
import numpy as np
import pandas as pd

from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework.authtoken.models import Token
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin, AbstractEmailAddress

from description_parser.Grammar import DescriptionParser
from beers.models import BeerLearning, Beer, RecommendedBeer
#from tf_model import k_means, cluster_indices, ids


class EmailAddress(AbstractEmailAddress):
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)


class DraughtPicksUser(SimpleEmailConfirmationUserMixin, AbstractUser):
    """
    This class defines the draught picks user
    """
    MALE_CHOICE = 'M'
    FEMALE_CHOICE = 'F'
    OTHER_CHOICE = 'O'

    GENDER_CHOICES = (
        (MALE_CHOICE, 'Male'),
        (FEMALE_CHOICE, 'Female'),
        (OTHER_CHOICE, 'Other')
    )

    REQUIRED_FIELDS = ['email', 'date_of_birth']
    email = m.EmailField(unique=True)
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date_of_birth = m.DateField()
    weight = m.IntegerField(help_text="Weight in pounds.", blank=True, null=True)
    gender = m.CharField(max_length=1, choices=GENDER_CHOICES, default=FEMALE_CHOICE)
    favorite_beers = m.ManyToManyField('beers.Beer', related_name='favorite_beers')
    recent_beers = m.ManyToManyField('beers.Beer', related_name='recent_beers', through='beers.RecentBeer')
    rated_beers = m.ManyToManyField('beers.Beer', related_name='rated_beers', through='beers.BeerRating')
    recommended_beers = m.ManyToManyField('beers.Beer', related_name='recommended_beers', through='beers.RecommendedBeer')

    def send_verification_email(self):
        cxt = {
            'domain_name': settings.CLIENT_DOMAIN
        }
        html_message = render_to_string('email/verification/verification.html', context=cxt)
        text_msg = render_to_string('email/verification/verification.txt', context=cxt)
        send_mail(
            'DraughtPicks.beer - Email Verification',
            text_msg,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            html_message=html_message
        )

class BeerPreferences(m.Model):
    """
    This class is the blueprint for the beer preference
    """
    uuid = m.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    abv_low = m.IntegerField(null=True, blank=True)
    abv_hi = m.IntegerField(null=True, blank=True)
    ibu_low = m.IntegerField(null=True, blank=True)
    ibu_hi = m.IntegerField(null=True, blank=True)
    like_description = m.TextField(null=True, blank=True)
    user = m.ForeignKey(DraughtPicksUser, related_name='beer_preferences', on_delete=m.PROTECT)
    created_at = m.DateTimeField(auto_now_add=True)
    beer_learning = m.OneToOneField('beers.BeerLearning', blank=True, null=True, on_delete=m.PROTECT)

    def save(self, *args, **kwargs):
        """
        This saves the beer preference object
        :param args:
        :param kwargs:
        :return:
        """
        parsed = {}
        if self.like_description:
            p = DescriptionParser(self.like_description, {})
            parsed = p.parse()
        if not self.beer_learning:
            self.beer_learning = BeerLearning.objects.create(**parsed)
        else:
            # fields to update are in parsed.keys() and only set to 1
            # The difference between beer_learning.fields and parsed.keys() is set to zero
            zeros = self.beer_learning.learning_fields - parsed.keys()
            for attr in zeros:
                setattr(self.beer_learning, attr, 0)
            for k, v in parsed.items():
                setattr(self.beer_learning, k, v)
            self.beer_learning.save()

        faves_and_desc = []
        cols = self.beer_learning.learning_fields
        faves_and_desc.append(map(lambda f: getattr(self.beer_learning, f), cols))

        faves_learn = map(lambda x: x.beer_learning, self.user.favorite_beers.all())
        faves_learn = map(lambda x: map(lambda f: getattr(x, f), cols), faves_learn)

        faves_and_desc += faves_learn

        user_d = pd.DataFrame(data=faves_and_desc, dtype=np.float32, columns=cols)

        # user_d = pd.read_csv("/Users/jake/PycharmProjects/untitled/data/user_desc.csv", header=0, dtype=np.float32)

        def predict_fn(features):
            """
            This method predicts various clusters based on the info given
            :param features:
            :return:
            """
            return tf.train.limit_epochs(
                tf.convert_to_tensor(np.array(features, dtype=np.float32)), num_epochs=1,
            )

        l = list(k_means.predict_cluster_index(lambda: predict_fn(user_d)))

        rec_beers = []

        for i, e in enumerate(cluster_indices):
            if e == l[0]:
                rec_beers.append(ids[i])
        beers = Beer.objects.filter(
            id__in=rec_beers).exclude(
                id__in=self.user.favorite_beers.values_list('id', flat=True))
        self.user.recommended_beers.clear()
        for b in beers:
            RecommendedBeer.objects.create(user=self.user, beer=b, percent_match=self.get_percent_match(b, cols))
        super(BeerPreferences, self).save(*args, **kwargs)

    def get_percent_match(self, beer, cols):
        """
        This method gets the match percentage for the beer
        :param beer:
        :param cols:
        :return:
        """
        user_learn = self.beer_learning
        beer_learn = beer.beer_learning
        num_features = len(cols)

        # Number of 1s in user description
        num_ind = len(list(filter(lambda x: getattr(user_learn, x) == 1, cols)))

        # Number of matched features between user and beer
        num_matches = len(list(filter(lambda x: ((getattr(user_learn, x) == 1) and (getattr(beer_learn, x) == 1)), cols)))

        return int((num_features - (num_ind - num_matches)) / num_features * 100)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    This method creates an authentication token for use
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Token.objects.create(user=instance)
        instance.send_verification_email()
