"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Test user endpoints.
"""

from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings
from unittest import skip

from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import EmailAddress


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
        # Must have at least one confirmed email
        email = self.user.email_address_set.first()
        email.confirmed_at = datetime.now()
        email.save()
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertTrue(status.is_success(r.status_code))

    def test_login_error(self):
        """
        This tests if the user can login when bad creds provided
        :return:
        """
        self.client.force_authenticate(user=None)  # Remove auth for login
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'wrong'}, format='json')
        self.assertTrue(status.is_client_error(r.status_code))

    def test_login_email_not_confirmed(self):
        """
        This tests if the user can login when bad creds provided
        :return:
        """
        self.client.force_authenticate(user=None)  # Remove auth for login
        self.user.email_address_set.update(confirmed_at=None)
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'wrong'}, format='json')
        self.assertTrue(status.is_client_error(r.status_code))

    def test_create(self):
        self.client.force_authenticate(user=None)  # Remove auth for create

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

    def test_send_confirmation_emaill(self):
        self.user.send_confirmation_email()
        self.assertTrue(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'DraughtPicks.beer - Email Confirmation')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_email_confirmation_success(self):
        self.client.force_authenticate(user=None)  # No auth needed
        self.assertFalse(self.user.is_confirmed)
        r = self.client.put('/api/dev/users/confirm-email', {
            'confirm_key': self.user.confirmation_key
        })
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertTrue(self.user.is_confirmed)

    def test_email_confirm_error(self):
        self.client.force_authenticate(user=None)  # No auth needed
        self.assertFalse(self.user.is_confirmed)
        r = self.client.put('/api/dev/users/confirm-email', {})
        self.assertTrue(status.is_client_error(r.status_code), r.status_code)

    def test_resend_confirm_email_error(self):
        self.client.force_authenticate(user=None)  # No auth needed
        r = self.client.post('/api/dev/users/resend-confirm-email', {
            "email": 't@t.com'
        })
        self.assertTrue(status.is_client_error(r.status_code), r.status_code)

    def test_resend_confirm_email_success(self):
        r = self.client.post('/api/dev/users/resend-confirm-email', {
            "email": self.user.email
        })
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertTrue(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'DraughtPicks.beer - Email Confirmation')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_password_reset_email_error(self):
        r = self.client.post('/api/dev/users/password-reset-email', {'email': 'test@test.com'})
        self.assertTrue(status.is_client_error(r.status_code))
        self.assertTrue(len(mail.outbox) is 0)

    def test_send_password_reset_email_success(self):
        EmailAddress.objects.create(email='test@test.com', user=self.user)
        r = self.client.post('/api/dev/users/password-reset-email', {'email': 'test@test.com'})
        self.assertTrue(status.is_success(r.status_code))
        self.assertTrue(len(mail.outbox) is 1)

    def test_change_password_success(self):
        old_pw = self.user.password
        b64 = urlsafe_base64_encode(bytearray(str(self.user.uuid), encoding='utf8')).encode().decode()
        token = default_token_generator.make_token(self.user)
        data = {
            'token': token,
            'b64': b64,
            'password': 'change',
            'confirm_password': 'change'
        }
        r = self.client.post('/api/dev/users/change-password', data)
        self.assertEqual(r.status_code, status.HTTP_200_OK, r.data)
        # Refresh the in memory user instance
        user = get_user_model().objects.get(uuid=self.user.uuid)
        self.assertNotEqual(user.password, old_pw)

    def test_change_password_failure(self):
        r = self.client.post('/api/dev/users/change-password', {})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, r.data)


class TestBeerProfile(APITestCase):

    fixtures = ['users/fixtures/users.json']

    def test_create(self):
        # self.client.force_authenticate(user=None)  # Remove auth for create
        r = self.client.post('/api/dev/beer-profiles', {
            'abv_low': 2,
            'abv_high': 10,
            'ibu_low': 12,
            'ibu_high': 20,
            'user': get_user_model().objects.first().uuid
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
