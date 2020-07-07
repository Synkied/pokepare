# api/tests.py

# Add these imports at the top
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from pokemons.models import Language
from pokemons.models import Pokemon
from pokemons.models import PokemonSpecies
from pokemons.models import PokemonSpeciesName

from rest_framework import status
from rest_framework.test import APIClient


# Define this after the ModelTestCase


class PokemonDRFTestCase(TestCase):
    """Test suite for the pokemon views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            'test_user', '', 'test_password')
        self.language_data = {
            'name': 'en',
            'iso639': 'en',
            'iso3166': 'us',
            'official': True,
            'local_name': 'English',
            'sprite': 'https://www.countryflags.io/us/flat/16.png'
        }
        language = Language.objects.create(
            **self.language_data
        )
        self.pokemon_species_data = {
            'name': 'Bulbasaur',
        }
        pokemon_species = PokemonSpecies.objects.create(
            **self.pokemon_species_data
        )
        new_poke_name = {
            'name': 'Bulbasaur',
            'language': language,
            'pokemon_species': pokemon_species
        }
        poke_sp_name, created = PokemonSpeciesName.objects.get_or_create(
            **new_poke_name
        )
        self.pokemon_data = {
            'id': 1,
            'name': "Bulbasaur",
            'number': 1,
            'pokemon_species': pokemon_species
        }
        _ = Pokemon.objects.create(**self.pokemon_data)

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
