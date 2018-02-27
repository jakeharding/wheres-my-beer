"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  carolynwichers

Test user endpoints.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class TestBeers(APITestCase):
    fixtures = ['beers/fixtures/beers.json']

    def setUp(self):
        self.beer = get_user_model().objects.first()

    def test_retrieve(self):
        r = self.client.get('/api/dev/beer/%s' % self.beer.uuid)
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEqual(self.beer.name, r.data.get('name'))


