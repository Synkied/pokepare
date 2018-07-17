# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
import django

from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump

import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError


def find_card(name, number_set):

    try:
        api = finding(config_file='ebay.yaml', domain='svcs.ebay.com', warnings=True)

        keywords = ['pokemon', 'card', name, number_set]
        # card.name card.number_in_set + '/' + set.total_number

        api_request = {
            'keywords': " ".join(keywords),
            'itemFilter': [
                # {'name': 'Condition',
                #  'value': 'Used'},
                # {'name': 'LocatedIn',
                #  'value': 'FR'},
                {'name': 'AvailableTo',
                 'value': 'FR'},
            ],
            # 'affiliate': {'trackingId': 1},
            'sortOrder': 'CountryDescending',
        }

        response = api.execute('findItemsAdvanced', api_request)

        # print(response.dict()["searchResult"]["_count"])

        items_list = []

        for items in response.dict()["searchResult"]["item"]:
            items_list.append(items)

        # print(items_list)
        return items_list

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    print("Finding samples for SDK version %s" % ebaysdk.get_version())
    find_card()
    # viewItemURL
    # title
    # itemId
