"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Test user endpoints.
"""

from datetime import datetime

from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import DraughtPicksUser


class TestUsers(APITestCase):
    """
    This class tests the user
    """
    fixtures = ['users/fixtures/users.json']

    def setUp(self):
        """
        This tests user creation by setting up the test
        :return:
        """
        self.user = get_user_model().objects.first()
        # Assume user is authenticated for testing.
        self.client.force_authenticate(user=self.user)
        email = self.user.email_address_set.first()
        email.set_at = datetime.utcnow()
        email.save()

    def test_login(self):
        """
        This tests if the user can login
        :return:
        """
        self.client.force_authenticate(user=None)  # Remove auth for login
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertTrue(status.is_success(r.status_code))

    def test_create(self):
        self.client.force_authenticate(user=None)  # Remove auth for create
        print(DraughtPicksUser.objects.all())

        r = self.client.post('/api/dev/users', {
            'username': 'admin2',
            'password': 'test',
            'email': 't@test.com',
            'date_of_birth': '1997-05-04'
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)

    def test_update(self):
        r = self.client.put('/api/dev/users/%s' % self.user.uuid, {
            'username': 'admin2',
            'password': 'test',
            'email': 't@t.com',
            'date_of_birth': '1997-04-20',
            'weight': 195,
            'favorite_beers': [],
            'recent_beers': [],
            'rated_beers': [],
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEquals(r.data.get('weight'), 195)

    def test_retrieve(self):
        """
        This tests the retrieval
        :return:
        """
        r = self.client.get('/api/dev/users/%s' % self.user.uuid)
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEqual(self.user.username, r.data.get('username'))

    def test_list(self):
        """
        This tests the user lists
        :return:
        """
        r = self.client.get('/api/dev/users')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        results = r.data.get('results')
        self.assertTrue(isinstance(results, list))
        self.assertTrue(len(results) is 1)
        self.assertEqual(self.user.username, results[0].get('username'))

    def test_send_verification_email(self):
        self.user.send_verification_email()
        self.assertTrue(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'DraughtPicks.beer - Email Verification')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_email_confirmation_success(self):
        self.client.force_authenticate(user=None)  # No auth needed
        self.assertFalse(self.user.is_confirmed)
        r = self.client.put('/api/dev/confirm-email', {
            'confirm_key': self.user.confirmation_key
        })
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertTrue(self.user.is_confirmed)

    def test_email_confirm_error(self):
        self.client.force_authenticate(user=None)  # No auth needed
        self.assertFalse(self.user.is_confirmed)
        r = self.client.put('/api/dev/confirm-email', {})
        self.assertTrue(status.is_client_error(r.status_code), r.status_code)



class TestBeerPrefs(APITestCase):

    fixtures = ['users/fixtures/users.json']

    def test_create(self):
        self.client.force_authenticate(user=None) # Remove auth for create
        r = self.client.post('/api/dev/preferences', {
            'abv_low': 2,
            'abv_high': 10,
            'ibu_low': 12,
            'ibu_high': 20,
            'user': get_user_model().objects.first().uuid
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
