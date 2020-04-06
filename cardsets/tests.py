# api/tests.py

# Add these imports at the top
from cardsets.models import CardSet

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# Define this after the ModelTestCase


class CardSetDRFTestCase(TestCase):
    """Test suite for the sets views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser('test_user', '', 'test_password')
        self.card_set_data = {'id': 1, 'name': "Base", 'code': "base1"}
        _ = CardSet.objects.create(**self.card_set_data)

    def test_api_can_get_a_card_set(self):
        """Test the api can get a given card_set."""
        card_set = CardSet.objects.get(**self.card_set_data)
        response = self.client.get(
            reverse(
                'cardset-detail',
                kwargs={'pk': card_set.id}
            ),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, card_set.name)

    def test_api_auth_user_can_update_a_card_set(self):
        """Test the api can update a given card_set."""

        # auth the superuser with update rights
        self.client.login(username='test_user', password='test_password')

        card_set = CardSet.objects.get(**self.card_set_data)

        change_card_set = {'name': "Base 1", 'code': "base1"}
        response = self.client.put(
            reverse(
                'cardset-detail',
                kwargs={'pk': card_set.id}
            ),
            change_card_set,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, change_card_set["name"])

    def test_api_non_auth_user_cant_update_a_card_set(self):
        """Test the api can get a given card_set."""
        card_set = CardSet.objects.get(**self.card_set_data)
        change_card_set = {'name': "Base 1"}
        response = self.client.put(
            reverse(
                'cardset-detail',
                kwargs={'pk': card_set.id}
            ),
            change_card_set,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
