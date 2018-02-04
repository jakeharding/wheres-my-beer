"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Test user endpoints.
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class TestUsers(APITestCase):

    fixtures = ['users/fixtures/users.json']

    def setUp(self):
        self.user = get_user_model().objects.first()
        # Assume user is authenticated for testing.
        self.client.force_authenticate(user=self.user)

    def test_login(self):
        self.client.force_authenticate(user=None) # Remove auth for login
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertTrue(status.is_success(r.status_code))

    def test_create(self):
        self.client.force_authenticate(user=None) # Remove auth for create
        r = self.client.post('/api/dev/users', {
            'username': 'admin2',
            'password': 'test',
            'date_of_birth': '1997-05-04'
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)

    def test_update(self):
        r = self.client.put('/api/dev/users/%s' % self.user.uuid, {
            'username': 'admin2',
            'password': 'test',
            'date_of_birth': '1997-04-20',
            'weight': 195
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEquals(r.data.get('weight'), 195)

    def test_retrieve(self):
        r = self.client.get('/api/dev/users/%s' % self.user.uuid)
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEqual(self.user.username, r.data.get('username'))

    def test_list(self):
        r = self.client.get('/api/dev/users')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        results = r.data.get('results')
        self.assertTrue(isinstance(results, list))
        self.assertTrue(len(results) is 1)
        self.assertEqual(self.user.username, results[0].get('username'))
