"""
local_settings.py - (C) Copyright - 2018

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J. Harding

Local settings are for environment specific settings like database config, debug mode, and any secret keys needed.
This is a minimal example to help setup development when using more than the default database settings.
"""
try:
    from .settings import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travisci',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

CORS_ORIGIN_WHITELIST = (
)

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgiref.inmemory.ChannelLayer",
#         "ROUTING": "draught_picks.events.routing.channel_routing",
#     },
# }
