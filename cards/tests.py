# api/tests.py

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from cards.models import Card

# Define this after the ModelTestCase


class CardTestCase(TestCase):
    """Test suite for the cards views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser('test_user', '', 'test_password')
        self.card_data = {'id': 272, 'name': "Venusaur EX", 'national_pokedex_number': 3, "card_set_code": "xyp"}
        venusaur = Card.objects.create(**self.card_data)

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

    def test_api_auth_user_can_update_a_card(self):
        """Test the api can update a given card."""

        # auth the superuser with update rights
        self.client.login(username='test_user', password='test_password')

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, change_card["name"])

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
