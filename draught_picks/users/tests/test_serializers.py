"""
test_serializers - (C) Copyright - 2020
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Test serializers in the users package.
"""
from uuid import uuid4

from django.test import TestCase
from django.utils.http import urlsafe_base64_encode
from rest_framework.exceptions import ValidationError

from users.serializers import PasswordResetSerializer


class TestPasswordResetSerializer(TestCase):

    def test_validate_b64_raises_error(self):
        under_test = PasswordResetSerializer(data={})
        with self.assertRaises(ValidationError) as e:
            under_test.validate_b64('new')
        self.assertEqual(e.exception.detail[0], 'An error occurred. Please check the input and try again.')

    def test_validate_b64_returns_uuid(self):
        uuid = uuid4()
        b64 = urlsafe_base64_encode(bytearray(str(uuid), encoding='utf8')).encode().decode()
        r = PasswordResetSerializer().validate_b64(b64)
        self.assertEqual(r, str(uuid))

    def test_validate_pw_returns_pw(self):
        under_test = PasswordResetSerializer(data={
            'confirm_password': 'new'
        })
        self.assertEqual(under_test.validate_password('new'), 'new')

    def test_validate_password_raises_error(self):
        under_test = PasswordResetSerializer(data={
            'password': 'old',
            'confirm_password': 'new'
        })
        with self.assertRaises(ValidationError) as e:
            under_test.validate_password('old')
        self.assertEqual(e.exception.detail[0], 'An error occurred. Please check the input and try again.')

