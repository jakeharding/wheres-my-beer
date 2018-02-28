"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Expose user models through a REST API.
"""

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny

from .models import DraughtPicksUser, BeerPreferences


class UserSerializer(ModelSerializer):

    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = DraughtPicksUser
        fields = ('uuid', 'username', 'email', 'weight', 'date_of_birth', 'password', 'first_name', 'last_name')


class UserViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = DraughtPicksUser.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )

    def get_queryset(self):
        """
        Only allow users access to their user instance.
        :return: queryset the user has access to.
        """
        if self.request.user.is_superuser:
            return DraughtPicksUser.objects.all()
        else:
            return DraughtPicksUser.objects.filter(id=self.request.user.id)


class BeerPreferencesSerializer(ModelSerializer):
    class Meta:
        model = BeerPreferences
        fields = ('uuid', 'abv_low', 'abv_hi', 'ibu_low', 'ibu_hi', 'like_description', 'user', 'created_at',)


class UserBeerPreferencesSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerPreferencesSerializer
    queryset = BeerPreferences.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )