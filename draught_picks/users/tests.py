"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Test user endpoints.
"""

from rest_framework.test import APITestCase
from rest_framework import status


class TestLogin(APITestCase):

    fixtures = ['users/fixtures/users.json']

    def test_login(self):
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertTrue(status.is_success(r.status_code))
