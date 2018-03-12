"""
loaddb.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Load the database from breweryDB.
"""


import concurrent.futures, os
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from beers.models import Beer


start_url = 'https://api.brewerydb.com/v2/beers?key=%s' % settings.BREWERY_DB_KEY


def load_page(page_num):
    # if page_num % 10 is 0:
    # print("Loading page: %d in process %d" % (page_num, os.getpid()))
    page = requests.get('%s&p=%d' % (start_url, page_num))
    page_json = page.json()
    if page.status_code is 200:
        print("loading page:", page_num)
        for beer in page_json["data"]:
            beer_data = {
                # "id": ((page_num - 1) * 50) + page_offset + 1,
                "name": beer.get("name"),
                "description": beer.get("description"),
                "abv": beer.get("abv"),
                "ibu": beer.get("ibu"),
                "name_of_api": "brewerydb",
                "api_id": beer.get("id")
            }
            Beer.objects.get_or_create(**beer_data)
    else:
        print("Not successful:", page.status_code, page)
        print(page.headers)
    page.close()
    return page_json['numberOfPages']


def load_page_block(page_start):
    # print("fetching page: ", DraughtPicksUser)
    # if page % 10 is 0:
    #     print("Fetching page:", page)
    with concurrent.futures.ThreadPoolExecutor() as thread_exec:
        try:
            thread_exec.map(load_page, range(page_start, page_start + 5))
        except KeyboardInterrupt:
            thread_exec.shutdown(wait=False)
    # p = requests.get('%s&p=%d' % (start_url, page)).json()
    # print(page, p['data'][0]['id'])
    # return p['data'][0]['id']


class Command(BaseCommand):

    #  sync example
    def handle(self, *args, **options):
        # print("Synchronous execution of loading db")
        # first = requests.get(start_url).json()
        total_pages = load_page(1)
        # Work here to save each beer to db
        for page in range(2, total_pages + 1):
            if page % 10 is 0:
                print("Fetching page:", page)
            load_page(page)
            # p = requests.get('%s&p=%d' % (start_url, page))
            # Work here to save beer to db

    #  async example
    # def handle(self, *args, **options):
    #     # print('Async loading of db using %d cpus' % cpu_count())
    #     first = requests.get('%s&p=101' % start_url)
    #     first_json = first.json()
    #     if first.status_code is 200:
    #         # print("loading page:", page_num)
    #         for beer in first_json["data"]:
    #             beer_data = {
    #                 # "id": ((page_num - 1) * 50) + page_offset + 1,
    #                 "name": beer.get("name"),
    #                 "description": beer.get("description"),
    #                 "abv": beer.get("abv"),
    #                 "ibu": beer.get("ibu"),
    #                 "name_of_api": "brewerydb",
    #                 "api_id": beer.get("id")
    #             }
    #             Beer.objects.get_or_create(**beer_data)
    #     else:
    #         print("Not successful:", first.status_code, first)
    #         print(first.headers)
    #     with concurrent.futures.ProcessPoolExecutor() as executor:
    #         try:
    #             executor.map(load_page_block, range(101, 201, 5))
    #         except KeyboardInterrupt:
    #             executor.shutdown(wait=False)
    #     pool = Pool(processes=cpu_count())
    #     pool.map(do_work, range(1, first['numberOfPages'] + 1))
