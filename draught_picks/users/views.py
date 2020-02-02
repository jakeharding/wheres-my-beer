"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Expose user models through a REST API.
"""

import logging

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from simple_email_confirmation.exceptions import EmailConfirmationExpired

from users.serializers import UserSerializer, BeerProfileSerializer, PasswordResetSerializer

from .models import DraughtPicksUser, BeerProfile, EmailAddress

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

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='change-password',
            serializer_class=PasswordResetSerializer)
    def change_password(self, request):
        serial = PasswordResetSerializer(data=request.data)
        if serial.is_valid(raise_exception=True):
            user = get_object_or_404(DraughtPicksUser, **{'uuid': serial.data.get('b64')})
            if default_token_generator.check_token(user, serial.data.get('token')):
                user.set_password(serial.data.get('password'))
                user.save()
                return Response(data=serial.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serial.errors)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='password-reset-email')
    def password_reset_email(self, request):
        email = EmailAddress.objects.filter(email=request.data.get('email')).first()
        if not email:
            raise ValidationError('Unable to send email.')
        email.send_password_reset_email()
        return Response({})

    @action(detail=False, methods=['put'], permission_classes=[AllowAny], url_path='confirm-email')
    def confirm_email(self, request):
        key = request.data.get('confirm_key')
        if not key:
            raise ValidationError()
        try:
            EmailAddress.objects.confirm(key)
        except (EmailConfirmationExpired, EmailAddress.DoesNotExist):
            raise ValidationError(
                {'confirm_key': 'The confirmation key submitted is expired or does not exist. '
                                'Please resend the confirmation email.'})
        return Response({})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='resend-confirm-email')
    def resend_confirm_email(self, request):
        user = DraughtPicksUser.objects.filter(email=request.data.get('email')).first()
        if not user:
            raise ValidationError({
                "email": "A record of that email address does not exist. Please register a user with the email address."
            })
        user.send_confirmation_email()
        return Response({"email": "Please check your inbox for the email."})


class BeerProfileViewSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerProfileSerializer
    queryset = BeerProfile.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )

    def get_queryset(self):
        """
        Only allow users access to their user instance.
        :return: queryset the user has access to.
        """
        return BeerProfile.objects.filter(user__id=self.request.user.id)


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
            'domain_name': settings.CLIENT_DOMAIN,  # To build URLs back to frontend
            'confirm_link': 'link',  # For email confirmation
            'to_email': 'test@test.com',
            'reset_link': 'reset'  # For password reset email
        })
        return kwargs


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        user = Token.objects.get(key=response.data.get('token')).user
        # If any email exists that has been confirmed, allow login
        if user.email_address_set.filter(confirmed_at__isnull=False).exists():
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'non_field_error': ['Unable to login. Have you confirmed your email address?']
        })
