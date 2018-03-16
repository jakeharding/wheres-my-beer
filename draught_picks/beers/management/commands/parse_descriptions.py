"""
parse_descriptions.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Parse all the descriptions in the database
"""

from concurrent import futures
from django.core.management.base import BaseCommand


from beers.models import Beer, BeerLearning


def worker(beer):
    beer.save()  # Calling save on a beer objects will create and save a  descriptoin


def worker_block(beers):
    with futures.ThreadPoolExecutor(max_workers=5) as thread_exec:
        thread_exec.map(worker, beers)


class Command(BaseCommand):

    # Asynchronous about 4 and half minutes
    def handle(self, *args, **kwargs):
        beers = Beer.objects.all()
        errors = []

        with futures.ProcessPoolExecutor() as executor:
            executor.map(worker_block, [beers[j:j + 5] for j in range(0, beers.count(), 5)])
        print("COMPLETE")
        print("ERRORS:", errors)

    # Synchronous about 13 minutes
    # def handle(self, *args, **options):
    #     total_parsed = 0
    #     total_errors = []
    #     for b in Beer.objects.filter(description__isnull=False).order_by('-pk'):
    #         parsed = {}
    #         try:
    #             new_parser = DescriptionParser(b.description)
    #             parsed = new_parser.parse()
    #             total_parsed += 1
    #         except DescriptionParseException as e:
    #             total_errors.append((b, e))
    #             print("ERROR:", b.name)
    #         b.beer_learning = BeerLearning.objects.create(**parsed)
    #         b.save()
    #     print("Total descriptions:", total_parsed)
    #     print("Total errors:", total_errors)
