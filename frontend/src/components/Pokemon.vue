<template>
  <v-container id="pokemons">
    <div>
      <template v-if="pokemon">
        <v-container>
          <ul>
            <li class="ns-li">
              <img :src="pokemon.front_sprite" :alt="pokemon.name">
            </li>
            <li class="ns-li">
              <p>#{{ pokemon.number }}</p>
              <p>{{ titleize(pokemon.name) }}</p>
            </li>
          </ul>
          <li class="ns-li" v-if="cards">
            <cards :cards="cards"></cards>
            <!-- <price-table :cards="cards.results"></price-table> -->
          </li>
        </v-container>
      </template>
      <template v-else>
        {{ errorMsg }}
      </template>

    </div>
  </v-container>
</template>

<script>
/* Imports */
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

import Cards from './Cards.vue'
import PriceTable from './PriceTable.vue'
import utils from '@/utils'

function capitalize (s) {
  return s && s[0].toUpperCase() + s.slice(1)
}

function onlyUnique (value, index, self) {
  return self.indexOf(value) === index
}

/* data, methods, components... declaration */
export default {
  components: {
    'cards': Cards,
    'price-table': PriceTable
  },
  data () {
    return {
      status: '',
      pokemon: null,
      cards: [],
      nextCardsPage: '',
      animated: false,
      errorMsg: null,
      cardSets: []
    }
  },
  title () {
    return `PokePare — ${this.pokemon.name}`
  },
  methods: {
    titleize: utils.titleize,
    getPokemonCards () {
      let thisVm = this
      let cardSetsList = []
      if (thisVm.$route.params) {
        thisVm.pokemon_name = thisVm.$route.params.name
      }
      const pokemonsUrl = this.$constants('pokemonsUrl')
      const cardsUrl = this.$constants('cardsUrl')

      const pokemonDetailUrl = `${pokemonsUrl}?insensitive_name=${capitalize(encodeURI(thisVm.pokemon_name))}`
      let pokemonId
      loadProgressBar()

      return axios.get(pokemonDetailUrl)
        .then(response => {
          if (response.data.count > 0) {
            thisVm.pokemon = response.data.results[0]
            thisVm.status = response.status
            pokemonId = response.data.results[0].id
            // filter to get only unique values in array
          } else {
            thisVm.errorMsg = 'No Pokémon found.'
          }
          const pokemonCardsUrl = `${cardsUrl}?pokemon_id=${pokemonId}`
          return axios.get(pokemonCardsUrl)
        })
        .then(response => {
          let cards = response.data
          for (var i = 0; i < cards.results.length; i++) {
            let cardPrices = utils.deepGet(cards.results[i], 'prices')
            if (cardPrices) {
              cardPrices.map(price => {
                let cardUniqueId = utils.deepGet(cards.results[i], 'unique_id')
                price.card_unique_id = `${cardUniqueId}`
              })
            }
            cardSetsList.push(cards.results[i].card_set_code)
          }
          thisVm.cardSets = cardSetsList.filter(onlyUnique)
          thisVm.cards = cards
          return cards
        })
        .catch(function (error) {
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error(error.response.data)
            console.error(error.response.status)
            console.error(error.response.headers)
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser
            // and an instance of http.ClientRequest in node.js
            console.error(error.request)
          } else {
            // Something happened in setting up the request that triggered an Error
            console.error('Error', error.message)
          }
          console.error(error.config)
        })
    }
  },
  async mounted () {
    await this.getPokemonCards()
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>

</style>
