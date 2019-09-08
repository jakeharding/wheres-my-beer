"""
serializers.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Serializers for users views.
"""
from django.contrib.auth.hashers import make_password
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from beers.models import Beer
from beers.views import BeerSerializer
from users.models import DraughtPicksUser, BeerPreferences


class BeerPreferencesSerializer(ModelSerializer):
    """
    This serializes the beer preferences
    """
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())

    class Meta:
        """
        This exposes the fields needed for the beer preferences serializer
        """
        model = BeerPreferences
        fields = ('uuid', 'abv_low', 'abv_hi', 'ibu_low', 'ibu_hi', 'like_description', 'user', 'created_at',)


class UserSerializer(ModelSerializer):
    """
    This is the user serializer
    """
    favorite_beers = BeerSerializer(many=True, required=False)
    recent_beers = BeerSerializer(many=True, required=False)
    rated_beers = BeerSerializer(many=True, required=False)

    def validate_password(self, value):
        """
        This validates the user's password
        :param value:
        :return:
        """
        if self.context.get('request').stream.method == "POST":
            value = make_password(value)
        return value

    def update(self, instance, validated_data):
        """
        This updates the user serialization
        :param instance:
        :param validated_data:
        :return:
        """
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
        """
        This exposes the fields needed for the user serialization
        """
        model = DraughtPicksUser
        exclude = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')