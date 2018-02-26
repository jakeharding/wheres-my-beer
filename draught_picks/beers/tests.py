"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  carolynwichers

Test user endpoints.
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class TestBeers(APITestCase):

    def setUp(self):
        self.beer = get_user_model().objects.first()

