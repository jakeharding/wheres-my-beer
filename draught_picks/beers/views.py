"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  carolynwichers

Expose user models through a REST API.
"""
from rest_framework.serializers import ModelSerializer, UUIDField, SlugRelatedField, SerializerMethodField
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


class BeerRatingSerializer(ModelSerializer):
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())
    uuid = UUIDField(read_only=True)

    class Meta:
        model = BeerRating
        fields = ('uuid', 'user', 'beer', 'rating', 'description', 'created_at',)


class BeerWithRatingSerializer(BeerSerializer):
    """
    Serializer to include the rating by the given user.
    """
    rating = SerializerMethodField()

    def __init__(self, data, user=None, **kwargs):
        super().__init__(data, **kwargs)
        self.user = user

    def get_rating(self, obj):
        return BeerRatingSerializer(BeerRating.objects.filter(beer=obj, user=self.user), many=True).data


class BeerSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'
    search_fields = ("name", )
    filter_backends = (SearchFilter, )


class BeerRatingSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerRatingSerializer
    queryset = BeerRating.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        return BeerRating.objects.filter(user=self.request.user)


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

    def list(self, request, *arg, **kwargs):
        """
        Override to serialize the beers and not the through table.
        :param request:
        :param arg:
        :param kwargs:
        :return:
        """
        qs = self.request.user.recent_beers.order_by('created_at')
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = BeerWithRatingSerializer(page, user=request.user, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BeerWithRatingSerializer(qs, user=request.user, many=True)
        return Response(serializer.data)
