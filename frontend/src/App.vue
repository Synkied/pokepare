<template>
  <v-app class="app-wrapper">
    <app-header></app-header>
    <v-content>
      <v-container class="body-container">
        <router-view/>
      </v-container>
      <app-footer></app-footer>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios'
import { mapMutations, mapState } from 'vuex'

import Header from './components/shared/Header.vue'
import Footer from './components/shared/Footer.vue'
import SearchBar from './components/SearchBar.vue'

import utils from '@/utils'

export default {
  name: 'App',
  components: {
    'app-header': Header,
    'app-footer': Footer,
    'search-bar': SearchBar
  },
  computed: {
    ...mapState([
      'userLanguage',
      'storedPokemons'
    ])
  },
  watch: {
    userLanguage: {
      handler (newVal, oldVal) {
        if (this.storedPokemons.length) {
          this.getPokemonNames(this.storedPokemons)
        }
      }
    }
  },
  methods: {
    ...mapMutations([
      'setPokemonsToStore'
    ]),
    async getPokemonNames (storedPokemons) {
      try {
        for (var i = storedPokemons.length - 1; i >= 0; i--) {
          let pokemonSpeciesResults = await axios.get(storedPokemons[i].pokemon_species)
          let pokemonSpeciesNames = utils.deepGet(pokemonSpeciesResults, 'data.names')
          for (var j = pokemonSpeciesNames.length - 1; j >= 0; j--) {
            let language = utils.deepGet(pokemonSpeciesNames[j], 'language.iso639')
            console.log(language, this.userLanguage)
            if (language === this.userLanguage) {
              storedPokemons[i].name = pokemonSpeciesNames[j].name
            }
          }
        }
        this.setPokemonsToStore(storedPokemons)
      } catch (err) {
        if (err.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error(err.response.data)
          console.error(err.response.status)
          console.error(err.response.headers)
        } else if (err.request) {
          // The request was made but no response was received
          // `err.request` is an instance of XMLHttpRequest in the browser
          // and an instance of http.ClientRequest in node.js
          console.error(err.request)
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error', err.message)
        }
        console.error(err.config)
      }
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Avenir');
@import url('https://fonts.googleapis.com/css?family=Oswald');
@import url('https://fonts.googleapis.com/css?family=Cabin');
@import url('https://fonts.googleapis.com/css?family=Raleway');
@import url('https://fonts.googleapis.com/css?family=Oxygen');
@import url('https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900');
@import url('https://fonts.googleapis.com/css?family=Material+Icons');
@import url('https://use.fontawesome.com/releases/v5.0.13/css/all.css');

/* Hide spinners for Firefox */
input[type=number] {
    -moz-appearance: textfield;
}

/* Hide spinners for Chrome */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
/*  background-color: #EEE;
*/}

.app-wrapper .container.body-container {
  padding-bottom: 100px;
}

#app .container {
  max-width: 1400px;
}

.v-application.app-wrapper a {
  text-decoration: none;
  color: #fff
}

a:hover {
  text-decoration: none;
}

.related-pokemon-image {
  width: 100px;
  margin: auto;
}

.pokemon-link p {
  margin: -10px 0 30px 0;
}

h1 {
  text-align: center;
  font-family: 'Cabin', sans-serif;
  font-weight: bold;
  font-size: 2.5rem;
  text-transform: uppercase;
  color: #000;
}

h2 {
  font-family: 'Cabin', sans-serif;
  font-size: 2rem;
  font-weight: 700;
}

h3 small {
  font-size: 60%;
  color: #6f6f6f;
  line-height: 0;
}

.ns-li {
  list-style-type: none;
}

.ns-li a {
  text-decoration: none;
}

.ns-li a:hover {
  text-decoration: none;
}

.ns-li p {
  text-align:center;
}

ul {
  padding: 0;
}

.v-data-table__wrapper table {
  color: #fff;
}

</style>
