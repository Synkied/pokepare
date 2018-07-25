from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os
import requests
import pprint

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

# import os
# import django

# # used to execute this file without django running
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokepare.settings")
# django.setup()


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # this ensures that the filename is not already used
        # when uploading a file
        self.delete(name)
        return name


class PriceFinder():

    def get_ebay_prices(self, name, number_in_set, set_name):

        items_list = []

        try:
            api = finding(
                config_file='ebay.yaml',
                domain='svcs.ebay.com',
                warnings=True)

            keywords = ['pokemon', 'card', name, number_in_set, set_name]
            # card.name card.number_in_set + '/' + set.total_number

            try:
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

                # needed_keys = [
                #     'condition',
                #     'shippingInfo',
                #     'sellingStatus',
                #     'title',
                #     'viewItemURL',
                # ]

                # needed_sub_keys = [
                #     'conditionDisplayName',
                #     'shipToLocations',
                #     'convertedCurrentPrice',
                #     'currentPrice',
                # ]

                # res = response.dict()["searchResult"]["item"]

                for item in response.dict()["searchResult"]["item"]:
                    # for key in needed_keys:
                    #     if key not in items.keys():
                    #         items[key] = "N/A"
                    # items_list.append(items)

                    item_dict = {}

                    item_dict["website"] = "eBay"
                    item_dict["link"] = item["viewItemURL"]
                    item_dict["market_price"] = float(item["sellingStatus"]["convertedCurrentPrice"]["value"])
                    item_dict["edition"] = "N/A"
                    item_dict["currency"] = item["sellingStatus"]["convertedCurrentPrice"]["_currencyId"]
                    item_dict["product_id"] = int(item["itemId"])
                    item_dict["condition"] = item["condition"]["conditionDisplayName"]
                    item_dict["set_name"] = 'N/A'

                    items_list.append(item_dict)

            except KeyError as kerr:
                pass

        except ConnectionError as e:
            print(e)
            print(e.response.dict())

        return items_list

    def get_tcgplayer_prices(self, name):

        token = settings.TCGPLAYER_BEARER_TOKEN
        product_url = ("http://api.tcgplayer.com/catalog/products?categoryId=3&productTypes=Cards&limit=100&productName=" + name)
        # esetting header for tcgplayer api bearer token
        headers = {"Authorization": "Bearer " + token}

        results = []

        try:
            # requests response object
            pokemon_response = requests.get(
                product_url, headers=headers).json()

            # only execute api calls if a product was found (success=true)
            if pokemon_response["success"] is True:

                # variables instanciation
                product_ids = [
                    result["productId"]
                    for result in pokemon_response["results"]
                ]
                group_ids = [
                    result["groupId"]
                    for result in pokemon_response["results"]
                ]

                # fetching groups (sets)
                group_url = (
                    "http://api.tcgplayer.com/catalog/groups/" +
                    ",".join(str(id) for id in group_ids)
                )
                groups_response = requests.get(
                    group_url, headers=headers).json()

                # fetching prices
                prices_url = (
                    "http://api.tcgplayer.com/pricing/product/" +
                    ",".join(str(id) for id in product_ids)
                )

                prices_response = requests.get(
                    prices_url, headers=headers).json()

                # little algorithm to join the aggregated data
                for result in pokemon_response["results"]:
                    prices_dict = {}
                    prices_dict["website"] = "TCGPlayer"
                    prices_dict["link"] = result["url"]
                    prices_dict["product_id"] = result["productId"]
                    prices_dict["condition"] = "N/A"
                    prices_dict["currency"] = "USD"
                    # group (sets) appending
                    for group in groups_response["results"]:
                        if group["groupId"] == result["groupId"]:
                            prices_dict["set_name"] = group["name"]

                    for prices in prices_response["results"]:
                        if prices["productId"] == result["productId"] and prices["marketPrice"] is not None:
                            prices_dict["market_price"] = prices["marketPrice"]
                            prices_dict["edition"] = prices["subTypeName"]

                    results.append(prices_dict)

                # add a count item to the data, to know the number of elems returned
                prices_dict["count"] = len(results)

        except KeyError as kerr:
            print("KeyError:", kerr, " Maybe the API key isn't valid anymore? Or a throttle occured?")

        return results


if __name__ == "__main__":
    pp = PriceFinder()

    result = pp.get_ebay_prices("Bulbasaur", '1', 'Shining Legends')

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)
