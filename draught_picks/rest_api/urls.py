"""
urls.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Constructs the urls for the REST API.
"""

from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, BeerProfileViewSet, LoginView
from beers.views import BeerSet, BeerRatingSet, RecentBeerSet, RecommendedBeerSet

router = DefaultRouter(trailing_slash=False)

router.register('users', UserViewSet)
router.register('beer-profiles', BeerProfileViewSet)
router.register('beers', BeerSet)
router.register('beer-ratings', BeerRatingSet)
router.register('recent-beers', RecentBeerSet)
router.register('recommended-beers', RecommendedBeerSet)

urlpatterns = [
    re_path(r'^login', LoginView.as_view()),
    re_path(r'', include(router.urls)),
]