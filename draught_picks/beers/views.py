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
from .models import Beer, BeerRating, RecentBeer, RecommendedBeer


class BeerSerializer(ModelSerializer):
    """
    Serializes the beer
    """
    uuid = UUIDField()

    class Meta:
        """
        Exposes the fields needed in order to serialize the beer
        """
        model = Beer
        fields = ('uuid', 'name', 'description', 'abv', 'ibu', 'api_id', 'name_of_api', 'created_at',)


class BeerRatingSerializer(ModelSerializer):
    """
    Serializes the beer rating
    """
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())
    uuid = UUIDField(read_only=True)

    class Meta:
        """
        Exposes the fields needed in order to serialize the beer rating
        """
        model = BeerRating
        fields = ('uuid', 'user', 'beer', 'rating', 'description', 'created_at',)


class RecommendedBeerSerializer(ModelSerializer):
    """
    Serializes the recommended beer
    """
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())
    uuid = UUIDField(read_only=True)

    class Meta:
        """
        Exposes the fields needed in order to serialize the beer rating
        """
        model = RecommendedBeer
        fields = ('uuid', 'user', 'beer', 'percent_match', 'agreed', 'created_at',)


class BeerWithRatingSerializer(BeerSerializer):
    """
    Serializer to include the rating by the given user.
    """
    rating = SerializerMethodField()
    recommended = SerializerMethodField()

    def __init__(self, instance, user=None, **kwargs):
        """
        Instantiates the beer rating serializer
        :param instance:
        :param user:
        :param kwargs:
        """
        self.user = user
        super().__init__(instance, **kwargs)

    def get_recommended(self, beer):
        """
        Gets a recommended beer
        :param beer:
        :return:
        """
        req = self.context.get('request')
        user = None
        if self.user:
            user = self.user
        elif req:
            user = req.user
        recommended = user.recommendedbeer_set.filter(beer=beer).first()
        if recommended:
            return RecommendedBeerSerializer(recommended).data
        return {}

    def get_rating(self, obj):
        """
        Gets a rating
        :param obj:
        :return:
        """
        req = self.context.get('request')
        ratings = []
        if self.user:
            ratings = BeerRating.objects.filter(beer=obj, user=self.user)
        elif req:
            ratings = BeerRating.objects.filter(beer=obj, user=req.user)
        return BeerRatingSerializer(ratings, many=True).data

    class Meta:
        """
        Exposes the fields needed in order to serialize the beer rating
        """
        model = Beer
        fields = ('uuid', 'rating', 'name', 'description',
                  'abv', 'ibu', 'api_id', 'name_of_api', 'created_at', 'recommended')


class BeerSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Creates a needed beer set
    """
    serializer_class = BeerWithRatingSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'
    search_fields = ("name", )
    filter_backends = (SearchFilter, )


class BeerRatingSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Creates a needed beer rating set
    """
    serializer_class = BeerRatingSerializer
    queryset = BeerRating.objects.all()
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        """
        Method used to create a beer rating set
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request.data['user'] = str(request.user.uuid)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        """
        Get the querysets
        :return:
        """
        return BeerRating.objects.filter(user=self.request.user)


class RecentBeerSerializer(ModelSerializer):
    """
    This class serializes recent beers
    """
    uuid = UUIDField(read_only=True)
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())

    class Meta:
        """
        Exposes the fields needed in order to serialize the recent beer
        """
        model = RecentBeer
        fields = ('uuid', 'user', 'beer', 'created_at',)


class BeerWithRecentSerializer(BeerWithRatingSerializer):
    """
    This class Serlizes the beer with the recent beer
    """
    recents = SerializerMethodField()

    def get_recents(self, obj):
        """
        This method gets the recent beer object
        :param obj:
        :return:
        """
        req = self.context.get('request')
        users = None
        if self.user:
            user = self.user
        elif req:
           user = req.user
        recents = user.recentbeer_set.filter(beer=obj)
        return RecentBeerSerializer(recents, many=True).data

    class Meta:
        """
        Exposes the fields needed in order to serialize the get recent beers
        """
        model = Beer
        fields = ('uuid', 'rating', 'name', 'description', 'abv', 'ibu', 'api_id', 'name_of_api', 'created_at', 'recents')


class RecentBeerSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """
    This class creates a recent beers set
    """
    serializer_class = RecentBeerSerializer
    queryset = RecentBeer.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        This method gets the queryset for the recent beer set
        :return:
        """
        return RecentBeer.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        This method will create a recent beer set
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request.data['user'] = str(request.user.uuid)
        return super().create(request, *args, **kwargs)

    def list(self, request, *arg, **kwargs):
        """
        Override to serialize the beers and not the through table.
        :param request:
        :param arg:
        :param kwargs:
        :return:
        """
        qs = self.request.user.recent_beers.distinct()
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = BeerWithRecentSerializer(page, user=request.user, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BeerWithRecentSerializer(qs, user=request.user, many=True)
        return Response(serializer.data)


class RecommendedBeerSet(ListModelMixin, GenericViewSet):
    """
    This class creates a recommended beer set
    """
    serializer_class = BeerWithRatingSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        """
        This gets the queryset for the recommended beer set
        :return:
        """
        return self.request.user.recommended_beers.order_by('-recommendedbeer__percent_match')
