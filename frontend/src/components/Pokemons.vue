<template>
  <v-container id="pokemons">
    <v-card tile flat outlined v-if="getPokemonsCount">
      <v-card-title class="secondary darken-1 headline">
        <template>
          <v-row class="justify-center">
            <v-col
              cols="2"
            >
              <span>
                {{ getPokemonsCount }} POKÉMON
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
              v-if="pokemonNbOfPages"
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
            v-for="pokemon in getPokemonsFromStore"
            :key="pokemon.id">
            <ul>
              <li class="ns-li">
                <router-link :to="{ name: 'pokemonDetail', params: { name: pokemon.name }}">
                  <img class="card-img" :src="pokemon.front_sprite" :alt="pokemon.local_name">
                </router-link>
              </li>
              <li class="ns-li">
                <p><router-link :to="{ name: 'pokemonDetail', params: { name: pokemon.name }}">{{ titleize(pokemon.local_name) }}</router-link></p>
              </li>
            </ul>
          </v-col>
        </v-row>
      </div>
      <v-pagination
        v-if="pokemonNbOfPages"
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
import { mapGetters, mapMutations, mapState } from 'vuex'

import utils from '@/utils'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      moduleTitle: 'Pokémon',
      perPageLimit: null,
      pageOffset: null,
      pokemons: [],
      pokemonPage: null,
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
        if (newVal && oldVal) {
          let curQuery = JSON.parse(JSON.stringify(this.$route.query))
          if (Number(curQuery['page']) !== newVal) {
            this.$router.replace({ path: this.$route.params[0], query: { ...curQuery, page: newVal } })
          }
          if (newVal > this.pokemonNbOfPages && this.pokemonNbOfPages > 0) {
            this.pokemonPage = this.pokemonNbOfPages
          }
          this.pageOffset = (this.perPageLimit * newVal) - this.perPageLimit
          this.getPokemonPage(this.pokemonPageUrl)
          this.setPokemonsPage(newVal)
        }
      }
    },
    perPageLimit: {
      handler (newVal, oldVal) {
        console.log(newVal, oldVal)
        let maxNumberPerPage = Math.max(...this.numberPerPage)
        if (newVal !== oldVal) {
          let curQuery = JSON.parse(JSON.stringify(this.$route.query))
          if (Number(curQuery['per_page']) !== newVal) {
            this.$router.replace({ path: this.$route.params[0], query: { ...curQuery, 'per_page': newVal } })
          }
          if (this.pokemonPage > this.pokemonNbOfPages && this.pokemonNbOfPages > 0) {
            this.pokemonPage = this.pokemonNbOfPages
          }
          if (newVal > maxNumberPerPage) {
            this.perPageLimit = maxNumberPerPage
          } else {
            this.pageOffset = (this.perPageLimit * this.pokemonPage) - this.perPageLimit
            this.getPokemonPage(this.pokemonPageUrl)
            this.setPokemonsByPage(newVal)
          }
        }
      }
    },
    userLanguage: {
      handler (newVal, oldVal) {
        this.getPokemonPage(this.pokemonPageUrl)
      }
    }
  },
  computed: {
    ...mapGetters([
      'getPokemonsFromStore',
      'getUserLanguage',
      'getPokemonsCount'
    ]),
    ...mapState([
      'userLanguage'
    ]),
    pokemonPageUrl () {
      return `${this.$constants('pokemonsUrl')}?limit=${this.perPageLimit}&offset=${this.pageOffset}&language=${this.getUserLanguage}`
    },
    pokemonNbOfPages () {
      return Math.round(this.getPokemonsCount / this.perPageLimit)
    }
  },
  methods: {
    titleize: utils.titleize,
    ...mapMutations([
      'setPokemonsToStore',
      'setPokemonsPage',
      'setPokemonsByPage',
      'setPokemonsCount'
    ]),
    async getPokemonPage (pokemonPageUrl) {
      console.log(pokemonPageUrl)
      try {
        let response = await axios.get(pokemonPageUrl)
        let pokemons = utils.deepGet(response, 'data.results', [])
        this.setPokemonsCount(response.data.count)
        this.setPokemonsToStore(pokemons)
        this.pageOffset = Number(utils.urlArgsParser(pokemonPageUrl)['offset']) || 0
        this.perPageLimit = Number(utils.urlArgsParser(pokemonPageUrl)['limit']) || 60
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
  async created () {
    let page = utils.deepGet(this.$route, 'query.page')
    this.pokemonPage = Number(page)
    this.perPageLimit = Number(utils.deepGet(this.$route, 'query.per_page'))
    this.pageOffset = (this.perPageLimit * Number(page)) - this.perPageLimit
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
.no-padding-text-field {
  padding: 0;
}
</style>
