# api/tests.py

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from sets.models import Set

# Define this after the ModelTestCase


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser('test_user', '', 'test_password')
        self.card_set_data = {'pk': 1, 'name': "Base", 'code': "base1"}
        base_card_set = Set.objects.create(**self.card_set_data)

    def test_api_can_get_a_card_set(self):
        """Test the api can get a given card_set."""
        card_set = Set.objects.get(**self.card_set_data)
        response = self.client.get(
            reverse(
                'set-detail',
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

        card_set = Set.objects.get(**self.card_set_data)

        change_card_set = {'name': "Base 1", 'code': "base1"}
        response = self.client.put(
            reverse(
                'set-detail',
                kwargs={'pk': card_set.id}
            ),
            change_card_set,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, change_card_set["name"])

    def test_api_non_auth_user_cant_update_a_card_set(self):
        """Test the api can get a given card_set."""
        card_set = Set.objects.get(**self.card_set_data)
        change_card_set = {'name': "Base 1"}
        response = self.client.put(
            reverse(
                'set-detail',
                kwargs={'pk': card_set.id}
            ),
            change_card_set,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
