# -*- coding: utf-8 -*-
from projects.tokens import token_generator
from rest_framework import permissions


class HasAPIAccess(permissions.BasePermission):
    """ """
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_token = request.META.get('HTTP_API_KEY', None)
        return bool(api_token and token_generator.check_token(api_token))
