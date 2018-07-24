# api/tests.py

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from pokemons.models import Pokemon

# Define this after the ModelTestCase


class PokemonDRFTestCase(TestCase):
    """Test suite for the pokemon views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser('test_user', '', 'test_password')
        self.pokemon_data = {'id': 1, 'name': "Bulbasaur", 'number': 1}
        bulbasaur = Pokemon.objects.create(**self.pokemon_data)

    def test_api_can_get_a_pokemon(self):
        """Test the api can get a given pokemon."""
        pokemon = Pokemon.objects.get(**self.pokemon_data)
        response = self.client.get(
            reverse(
                'pokemon-detail',
                kwargs={'pk': pokemon.id}
            ),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, pokemon.name)

    def test_api_auth_user_can_update_a_pokemon(self):
        """Test the api can update a given pokemon."""

        # auth the superuser with update rights
        self.client.login(username='test_user', password='test_password')

        pokemon = Pokemon.objects.get(**self.pokemon_data)

        change_pokemon = {'id': 1, 'name': "Bulbizarre", 'number': 1}
        response = self.client.put(
            reverse(
                'pokemon-detail',
                kwargs={'pk': pokemon.id}
            ),
            change_pokemon,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, change_pokemon["name"])

    def test_api_non_auth_user_cant_update_a_pokemon(self):
        """Test the api can get a given pokemon."""
        pokemon = Pokemon.objects.get(**self.pokemon_data)
        change_pokemon = {'id': 1, 'name': "Bulbizarre", 'number': 1}
        response = self.client.put(
            reverse(
                'pokemon-detail',
                kwargs={'pk': pokemon.id}
            ),
            change_pokemon,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
