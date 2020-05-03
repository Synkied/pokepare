<template>
  <v-container id="pokemons">
    <v-card tile flat outlined>
      <v-card-title class="secondary darken-1 headline" v-if="dataCount">
        {{ dataCount }} POKÉMON
      </v-card-title>
      <v-divider class="mb-5"></v-divider>
      <v-btn
        outlined
        ref="previous"
        class="mt-5"
        :disabled="pageNumber === 0 || disable"
        @click="prevPage">
          Prev
      </v-btn>
      <v-btn
        outlined
        ref="next"
        class="mt-5"
        :disabled="pageNumber >= pageCount -1 || disable"
        @click="nextPage">
          Next
      </v-btn>
      <div>
        <v-row v-if="pokemons">
          <v-col
            cols="4"
            md="2"
            v-for="pokemon in paginatedData"
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
    </v-card>
  </v-container>
</template>

<script>
/* Imports */
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      dataCount: '',
      status: '',
      animated: false,
      errorMsg: null,
      moduleTitle: 'Pokémon',
      next: '',
      previous: '',
      pageNumber: 0,
      limit: '',
      pokemons: '',
      disable: false
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  props: {
    size: {
      type: Number,
      required: false,
      default: 60
    }
  },
  computed: {
    pageCount () {
      let l = this.dataCount
      let s = this.size
      return Math.ceil(l / s)
    },
    paginatedData () {
      const start = this.pageNumber * this.size
      const end = start + this.size
      return this.pokemons.slice(start, end)
    }
  },
  methods: {
  /* viewMore () {
      axios.get(this.next).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.next = response.data.next
      })
    }, */
    nextPage () {
      this.disable = true
      axios.get(this.next)
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            this.pokemons.push(response.data.results[i])
            this.disable = false
          }
          this.next = response.data.next
        })
      this.pageNumber++
      if (this.pokemons.length === this.dataCount) {
        this.disable = false
      }
    },
    prevPage () {
      axios.get(this.previous).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.previous = response.data.previous
      })
      this.pageNumber--
    }
  },
  components: {
  },
  mounted () {
    const pokemonsUrl = this.$constants('pokemonsUrl')
    loadProgressBar()
    axios.get(pokemonsUrl).then(response => {
      if (response.data) {
        this.next = response.data.next
        this.pokemons = response.data.results
        this.dataCount = response.data.count
        this.status = response.status
        this.limit = Number(this.next.substring(this.next.indexOf('=') + 1, this.next.indexOf('&')))
      }
    })
      .catch(function (error) {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.log(error.response.data)
          console.log(error.response.status)
          console.log(error.response.headers)
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser
          // and an instance of http.ClientRequest in node.js
          console.log(error.request)
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log('Error', error.message)
        }
        console.log(error.config)
      })
  },
  goToView (routeName, routeParams) {
    this.$router.push({ name: routeName, params: routeParams })
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
