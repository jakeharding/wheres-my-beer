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

from openpyxl import load_workbook

from beers.models import Beer
from description_parser.Grammar import DescriptionParser, DescriptionParseException


def worker(beer):
    parser = DescriptionParser(beer.description)
    parser.parse()
    # TODO save the machine learning table here


def worker_block(beers):
    with futures.ThreadPoolExecutor(max_workers=5) as thread_exec:
        thread_exec.map(worker, beers)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        beers = Beer.objects.filter(description__isnull=False).all()

        with futures.ProcessPoolExecutor() as executor:
            executor.map(worker_block, [beers[j-5:j] for j in range(5, beers.count(), 5)])

    # def handle(self, *args, **options):
    #     total_parsed = 0
    #     total_errors = []
    #     for b in Beer.objects.filter(description__isnull=False).order_by('-pk'):
    #         try:
    #             new_parser = DescriptionParser(b.description)
    #             new_parser.parse()
    #             total_parsed += 1
    #         except DescriptionParseException as e:
    #             total_errors.append((b, e))
    #             print("ERROR:", b.name)
    #     print("Total descriptions:", total_parsed)
    #     print("Total errors:", total_errors)
