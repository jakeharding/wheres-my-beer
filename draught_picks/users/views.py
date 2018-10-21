"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Expose user models through a REST API.
"""

import logging

from django.views.generic.base import TemplateView
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from users.serializers import UserSerializer, BeerPreferencesSerializer

from .models import DraughtPicksUser, BeerPreferences, EmailAddress

logger = logging.getLogger('users.views')


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
        return DraughtPicksUser.objects.filter(id=self.request.user.id)


class UserBeerPreferencesSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerPreferencesSerializer
    queryset = BeerPreferences.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )

    def get_queryset(self):
        """
        Only allow users access to their user instance.
        :return: queryset the user has access to.
        """
        return BeerPreferences.objects.filter(user__id=self.request.user.id)


@api_view(['PUT'])
@permission_classes([AllowAny])
def confirm_email(request):
    key = request.data.get('confirm_key')
    if not key:
        raise ValidationError()
    EmailAddress.objects.confirm(key)
    return Response()


class EmailTemplateView(TemplateView):
    """
    View to render email templates in the browser to help development.
    Email templates must use inline styles only! Use premailer!
    """
    def get_template_names(self):
        name = self.kwargs.get('name', '')
        return ['email/%s/%s.html' % (name, name)]

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'domain_name': settings.CLIENT_DOMAIN,
            'verify_link': 'link',
            'to_email': 'test@test.com',
        })
        return kwargs
