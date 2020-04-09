# api/tests.py
import json
from unittest.mock import Mock
from unittest.mock import patch

from cards.models import Card

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from utils import PriceFinder


class CardDRFTestCase(TestCase):
    """Test suite for the cards views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            'test_user', '', 'test_password'
        )
        self.card_data = {
            'id': 272,
            'name': "Venusaur EX",
            'national_pokedex_number': 3,
            "card_set_code": "xyp"
        }
        _ = Card.objects.create(**self.card_data)

    def test_api_can_get_a_card(self):
        """Test the api can get a given card."""
        card = Card.objects.get(**self.card_data)
        response = self.client.get(
            reverse(
                'card-detail',
                kwargs={'pk': card.id}
            ),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, card.name)

    # def test_api_auth_user_can_update_a_card(self):
    #     """Test the api can update a given card."""

    #     # auth the superuser with update rights
    #     self.client.login(username='test_user', password='test_password')

    #     card = Card.objects.get(**self.card_data)

    #     change_card = {'name': "Florizarre EX"}
    #     response = self.client.put(
    #         reverse(
    #             'card-detail',
    #             kwargs={'pk': card.id}
    #         ),
    #         change_card,
    #         format="json"
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertContains(response, change_card["name"])

    def test_api_non_auth_user_cant_update_a_card(self):
        """Test the api can get a given card."""
        card = Card.objects.get(**self.card_data)
        change_card = {'name': "Florizarre EX"}
        response = self.client.put(
            reverse(
                'card-detail',
                kwargs={'pk': card.id}
            ),
            change_card,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CardPricesDataTestCase(TestCase):

    def setUp(self):
        self.token = settings.TCGPLAYER_BEARER_TOKEN
        self.price_finder = PriceFinder()
        self.name = "Charizard G"
        self.number_in_set = "20"
        self.set_name = "Supreme Victors"

        with open(
            "mock_data/tcgplayer_mock.json", "r", encoding="utf8"
        ) as mockfile:
            self.tcg_mock_data = json.load(mockfile)

    def test_instance(self):
        """
        :Test success conditions:
        The data returned is a valid GMapsRequest object
        """
        assert(isinstance(self.price_finder, PriceFinder))

    @patch('utils.PriceFinder.get_ebay_prices')
    def test_status_code_from_ebay(self, mock_get):
        """Mocking using a decorator"""

        # Mock status code of response.
        mock_get.return_value.status_code = 200
        response = self.price_finder.get_ebay_prices(
            self.name,
            self.number_in_set,
            self.set_name
        )

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 200)

    @patch('utils.PriceFinder.get_tcgplayer_prices')
    def test_retrieve_prices_from_tcgplayer(self, mock_get_data):
        mock_get_data.return_value = Mock()
        mock_get_data.return_value.json.return_value = self.tcg_mock_data
        data = self.price_finder.get_tcgplayer_prices(self.name)
        self.assertEqual(data.json.return_value, self.tcg_mock_data)
