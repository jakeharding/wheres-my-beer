"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Expose user models through a REST API.
"""

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny

from .models import DraughtPicksUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = DraughtPicksUser
        fields = ('uuid', 'username', 'email', 'weight', 'date_of_birth',)


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

