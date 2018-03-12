"""
parse_descriptions.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Parse all the descriptions in the database
"""


from django.core.management.base import BaseCommand

from beers.models import Beer
from description_parser.Grammar import DescriptionParser


class Command(BaseCommand):

    def handle(self, *args, **options):
        total_parsed = 0
        for b in Beer.objects.all():
            if b.description:
                new_parser = DescriptionParser(b.description)
                print(new_parser.parse())
                total_parsed += 1

        print("Total descriptions:", total_parsed)
