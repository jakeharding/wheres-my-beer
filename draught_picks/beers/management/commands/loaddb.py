"""
loaddb.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Load the database from breweryDB.
"""


from openpyxl import load_workbook

from django.conf import settings
from django.core.management.base import BaseCommand

from beers.models import Beer


start_url = 'https://api.brewerydb.com/v2/beers?key=%s' % settings.BREWERY_DB_KEY


class Command(BaseCommand):

    # Load database from spreadsheet using openpyxl.
    # Use pip install openpyxl to install but don't save it to the requirements file.
    # Assumes the spreadsheet is in the project root
    def handle(self, *args, **options):
        wb = load_workbook(settings.BASE_DIR + '/../output.xlsx')
        sheet = wb['Sheet1']
        for beer in sheet.rows:
            beer_data = {
                "name": beer[2].value,
                "api_id": beer[1].value,
                "abv": beer[3].value,
                "ibu": beer[4].value,
                "description": beer[9].value
            }
            try:
                Beer.objects.create(**beer_data)
            except Exception as e:
                print(e)
                print(beer[1].value)
