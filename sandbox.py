import os
import django
import pprint
# import re
# import functools
# import operator
import requests

from django.conf import settings

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


# used to execute this file without django running
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokepare.settings")
django.setup()

from cards.models import Card


# from pokemons.models import Pokemon
# from cards.models import Card
# from django.db.models import Q


# card = Card.objects.filter(name="Entei & Raikou LEGEND").first()

# q = re.split(r"[\W+|_']+", card.name)
# # remove chars between words, including "_"
# query = functools.reduce(
#     operator.or_, (
#         Q(
#             name__iexact=item
#         ) for item in q if len(item) > 1)
#     # if to not include unown with other cards
# )

# pok = Pokemon.objects.filter(query).order_by('id').first()
# print(pok.name)

# needed_keys = ['condition', 'shippingInfo', 'sellingStatus', 'title', 'viewItemURL']
# needed_sub_keys = ['conditionDisplayName', 'shipToLocations', 'convertedCurrentPrice', 'currentPrice']

# d = {
#     "title": "Bulbasaur 55/112 Non-Holo EX Fire Red & Leaf Green Pokemon Card ~ Near Mint",
#     "itemId": "142851178688",
#     "autoPay": "false",
#     "country": "US",
#     "globalId": "EBAY-US",
#     "location": "Holbrook,NY,USA",
#     "galleryURL": "http://thumbs1.ebaystatic.com/m/m7au1frrjoIwDCfP-Ffvh_A/140.jpg",
#     "postalCode": "11741",
#     "listingInfo": {
#         "gift": "false",
#         "endTime": "2018-08-01T03:11:43.000Z",
#         "startTime": "2018-07-02T03:11:43.000Z",
#         "listingType": "StoreInventory",
#         "bestOfferEnabled": "false",
#         "buyItNowAvailable": "false"
#     },
# }


# def walk_dict(d):
#     for key in needed_keys:
#         if key not in d.keys():
#             d[key] = "N/A"
#     for k, v in d.items():
#         if isinstance(v, dict):
#             print(k)
#             walk_dict(v)
#         else:
#             print("%s %s" % (k, v))


# walk_dict(d)

token = settings.TCGPLAYER_BEARER_TOKEN
endpoint = "http://api.tcgplayer.com/catalog/products?categoryId=3&productTypes=Cards&productName='Charizard'&limit=100"

headers = {"Authorization": "Bearer " + token}

pokemon_response = requests.get(endpoint, headers=headers).json()

results = []

product_ids = [result["productId"] for result in pokemon_response["results"]]
group_ids = [result["groupId"] for result in pokemon_response["results"]]

group_urls = "http://api.tcgplayer.com/catalog/groups/" + ",".join(str(id) for id in group_ids)

groups_response = requests.get(group_urls, headers=headers).json()

market = "http://api.tcgplayer.com/v1.8.1/pricing/product/" + ",".join(str(id) for id in product_ids)

prices_response = requests.get(market, headers=headers).json()

print(prices_response)

results = []

for result in pokemon_response["results"]:
    d = {"prices": []}
    d["link"] = result["url"]
    d["product_id"] = result["productId"]
    # group (sets) appending
    for group in groups_response["results"]:
        if group["groupId"] == result["groupId"]:
            d["group"] = {**group}

    for prices in prices_response["results"]:
        if prices["productId"] == result["productId"] and prices["marketPrice"] is not None:
            d["prices"].append({**prices})

    results.append(d)

d["zz"] = len(results)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(results)

# es = Elasticsearch(hosts=[{"host": 'elasticsearch'}])
# ses = SignatureES(es, distance_cutoff=0.3)

# img_base_dir = settings.MEDIA_ROOT

# img_dir = img_base_dir + '/cards/'

# dirlist = os.listdir(img_dir)

# for file in dirlist:
#     img_path = img_dir + file
#     print(img_path)
#     # t = ses.add_image(img_path)

# search = ses.search_image("https://images-na.ssl-images-amazon.com/images/I/71FkBOAGixL._SY450_.jpg")

# print(search)

# for result in search:
#     image_name_ext = result['path'].split('/')[-1::]
#     image_name = "".join(image_name_ext).split('.')[-2::][0]
#     print(image_name)

# p = Card.objects.get(unique_id=image_name)

# print(p)
