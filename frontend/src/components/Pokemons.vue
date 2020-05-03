<template>
  <v-container id="pokemons">
    <v-card tile flat outlined>
      <v-card-title class="secondary darken-1 headline" v-if="pokemonCount">
        <template>
          <v-row class="justify-center">
            <v-col
              cols="2"
            >
              <span>
                {{ pokemonCount }} POKÉMON
              </span>
            </v-col>
            <v-spacer></v-spacer>
            <v-col
              cols="6"
            >
            </v-col>
          </v-row>
        </template>
      </v-card-title>
      <v-divider class="mb-5"></v-divider>
      <v-container>
        <v-row class="justify-center">
          <v-col
            cols="4"
          >
            <v-pagination
              v-model="pokemonPage"
              :length="pokemonNbOfPages"
              next-icon="arrow_right"
              prev-icon="arrow_left"
              total-visible="8"
            >
            </v-pagination>
          </v-col>
          <v-col
            cols="1"
            >
            <v-autocomplete
              type="number"
              class="no-padding-text-field"
              :items="numberPerPage"
              label="Per page"
              v-model="perPageLimit"
            >
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-container>
      <div>
        <v-row v-if="pokemons">
          <v-col
            cols="4"
            md="3"
            v-for="pokemon in pokemons"
            :key="pokemon.id">
            <ul>
              <li class="ns-li">
                <router-link :to="{ name: 'pokemonDetail', params: { name: pokemon.name }}">
                  <img class="card-img" :src="pokemon.image" :alt="pokemon.name">
                </router-link>
              </li>
              <li class="ns-li">
                <p><router-link :to="{ name: 'pokemonDetail', params: { name: pokemon.name }}">{{ pokemon.name }}</router-link></p>
              </li>
            </ul>
          </v-col>
        </v-row>
      </div>
      <v-pagination
        v-model="pokemonPage"
        :length="pokemonNbOfPages"
        next-icon="arrow_right"
        prev-icon="arrow_left"
        total-visible="6"
      >
      </v-pagination>
    </v-card>
  </v-container>
</template>

<script>
/* Imports */
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

import utils from '@/utils'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      pokemonCount: '',
      moduleTitle: 'Pokémon',
      perPageLimit: 60,
      pageOffset: 0,
      pokemons: [],
      pokemonPage: 1,
      pokemonNbOfPages: 0,
      numberPerPage: [
        20,
        60,
        100
      ]
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  watch: {
    pokemonPage: {
      handler (newVal, oldVal) {
        if (newVal) {
          let curQuery = JSON.parse(JSON.stringify(this.$route.query))
          if (Number(curQuery['page']) !== newVal) {
            this.$router.replace({ path: this.$route.params[0], query: { ...curQuery, page: newVal } })
          }
          let perPageLimit = this.perPageLimit
          let pageOffset = (this.perPageLimit * newVal) - this.perPageLimit
          let pokemonPageUrl = `${this.$constants('pokemonsUrl')}?limit=${perPageLimit}&offset=${pageOffset}`
          this.getPokemonPage(pokemonPageUrl)
        }
      }
    },
    perPageLimit: {
      handler (newVal, oldVal) {
        if (newVal && oldVal) {
          let curQuery = JSON.parse(JSON.stringify(this.$route.query))
          if (Number(curQuery['per-page']) !== newVal) {
            this.$router.replace({ path: this.$route.params[0], query: { ...curQuery, 'per-page': newVal } })
          }
          let perPageLimit = this.perPageLimit
          let pageOffset = (this.perPageLimit * this.pokemonPage) - this.perPageLimit
          let pokemonPageUrl = `${this.$constants('pokemonsUrl')}?limit=${perPageLimit}&offset=${pageOffset}`
          this.getPokemonPage(pokemonPageUrl)
        }
      }
    }
  },
  methods: {
    async getPokemons () {
      const pokemonsUrl = `${this.$constants('pokemonsUrl')}?limit=${this.perPageLimit}&offset=${this.pageOffset}`
      loadProgressBar()
      await this.getPokemonPage(pokemonsUrl)
    },
    async getPokemonPage (pokemonPageUrl) {
      try {
        let response = await axios.get(pokemonPageUrl)
        if (response.data) {
          this.pokemons = response.data.results
          this.pokemonCount = response.data.count
          this.perPageLimit = Number(utils.urlArgsParser(pokemonPageUrl)['limit']) || 60
          this.pageOffset = Number(utils.urlArgsParser(pokemonPageUrl)['offset']) || 0
          this.pokemonNbOfPages = Math.round(this.pokemonCount / this.perPageLimit)
        }
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
  },
  async mounted () {
    await this.getPokemons()
    let page = utils.deepGet(this.$route, 'query.page')
    let perPage = utils.deepGet(this.$route, 'query.per-page')
    if (page && parseInt(page, 10) && page <= this.pokemonNbOfPages) {
      this.pokemonPage = Number(page)
    } else {
      this.pokemonPage = 1
    }
    if (perPage && parseInt(perPage, 10) && perPage <= this.pokemonCount) {
      this.perPageLimit = Number(perPage)
    }
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
.no-padding-text-field {
  padding: 0;
}
</style>
