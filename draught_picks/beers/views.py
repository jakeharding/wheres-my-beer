"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  carolynwichers

Expose user models through a REST API.
"""
from rest_framework.serializers import ModelSerializer, UUIDField, SlugRelatedField
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from users.models import DraughtPicksUser
from .models import Beer, BeerRating, RecentBeer


class BeerSerializer(ModelSerializer):
    uuid = UUIDField(read_only=True)

    class Meta:
        model = Beer
        exclude = ('id', )


class BeerSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'
    search_fields = ("name", )
    filter_backends = (SearchFilter, )


class BeerRatingSerializer(ModelSerializer):
    class Meta:
        model = BeerRating
        fields = ('uuid', 'user', 'beer', 'rating', 'description', 'created_at',)


class BeerRatingSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerRatingSerializer
    queryset = BeerRating.objects.all()
    lookup_field = 'uuid'


class RecentBeerSerializer(ModelSerializer):
    uuid = UUIDField(read_only=True)
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())

    class Meta:
        model = RecentBeer
        fields = ('uuid', 'user', 'beer', 'created_at',)


class RecentBeerSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RecentBeerSerializer
    queryset = RecentBeer.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        return RecentBeer.objects.filter(user=self.request.user)

    def list(self, *arg, **kwargs):
        """
        Override to serialize the beers and not the through table.
        :param arg:
        :param kwargs:
        :return:
        """
        qs = self.request.user.recent_beers.all()
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = BeerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BeerSerializer(qs, many=True)
        return Response(serializer.data)
