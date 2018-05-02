"""
parse_descriptions.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Parse all the descriptions in the database
"""

from django.core.management.base import BaseCommand

from beers.models import Beer, BeerLearning


class Command(BaseCommand):
    """
    This class will parse all the descriptions in the database
    """
    def handle(self, *args, **options):
        """
        Description: Parse all the descriptions in the database
        :param args:
        :param options:
        :return:
        """
        total_parsed = 0
        total_errors = []
        for b in Beer.objects.all():
            b.save() # Calling save on the beer will trigger the parse.
        print("Total descriptions:", total_parsed)
        print("Total errors:", total_errors)
