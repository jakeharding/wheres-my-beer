"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Expose user models through a REST API.
"""

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, UUIDField
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny

from beers.views import BeerSerializer
from beers.models import Beer

from .models import DraughtPicksUser, BeerPreferences


class UserSerializer(ModelSerializer):

    favorite_beers = BeerSerializer(many=True, required=False)
    recent_beers = BeerSerializer(many=True, required=False)
    rated_beers = BeerSerializer(many=True, required=False)

    def validate_password(self, value):
        return make_password(value)

    def update(self, instance, validated_data):
        faves = validated_data.pop('favorite_beers')

        # TODO save the recents and rated also
        validated_data.pop('recent_beers')
        validated_data.pop('rated_beers')
        fave_uid = list(map(lambda beer: beer.get('uuid'), faves))
        fave_objs = Beer.objects.filter(uuid__in=fave_uid)
        instance.favorite_beers.set(fave_objs)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = DraughtPicksUser
        exclude = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')


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