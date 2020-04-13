<template>
  <div id="cards">
    <div>
      <v-container v-if="card">
        <v-card flat outlined>
          <ul>
            <h3 class="card-title">{{ card.name }} - <a :href="'/cardsets/' + card.card_set_code">{{ card.card_set }}</a>
              <small>{{ card.number_in_set }}</small>
            </h3>
            <li class="ns-li">
              <img :src="card.image" :alt="card.name">
            </li>
          </ul>
          <div class="related-pokemon-image">
            <a :href="pokemon.url" class="pokemon-link">
              <img :src="pokemon.image" :alt="pokemon.name">
              <p v-if="pokemon.number < 10">#00{{ pokemon.number }}</p>
              <p v-else-if="pokemon.number < 100">#0{{ pokemon.number }}</p>
              <p v-else>#{{ pokemon.number }}</p>
            </a>
          </div>
          <price-table :cards="[card]"></price-table>
        </v-card>
      </v-container>
    </div>
  </div>
</template>

<script>
/* Imports */
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

import PriceTable from './PriceTable.vue'
import utils from '@/utils'

/* data, methods, components... declaration */
export default {
  components: {
    'price-table': PriceTable
  },
  data () {
    return {
      headers: [
        { text: 'Card id', value: 'card_unique_id' },
        { text: 'Website', value: 'website' },
        { text: 'Condition', value: 'condition' },
        { text: 'Edition', value: 'edition' },
        { text: 'URL', value: 'link' },
        { text: 'Current Price', value: 'market_price' },
        { text: 'Currency', value: 'currency' },
        { text: '', value: 'copy_row', sortable: false, align: 'end', width: '1%' }
      ],
      tableOptions: {
        itemsPerPage: 25
      },
      status: '',
      card: '',
      cardId: '',
      prevPokemon: '',
      pokemon: '',
      pokemonId: '',
      nextPokemon: '',
      errorMsg: null,
      numberInCardSet: '',
      totalNoCardSet: '',
      uniqueNumInSet: '',
      items: [],
      searchQuery: '',
      selectedWebsites: '',
      selectedConditions: '',
      selectedEditions: '',
      selectedCurrencies: '',
      rowCopyTooltipText: 'Copy row'
    }
  },
  title () {
    return `PokePare — ${this.card.name}`
  },
  watch: {
    card: function (newVal, oldVal) {
      this.addCardToStorage(newVal)
    }
  },
  computed: {
    orderedPrices () {
      let sortedCardPrices = JSON.parse(JSON.stringify(this.card.prices))
      sortedCardPrices = sortedCardPrices.sort((a, b) => {
        return a.market_price - b.market_price
      })
      return sortedCardPrices
    }
  },
  methods: {
    async getCardData () {
      var thisVm = this
      if (thisVm.$route.params) {
        thisVm.cardId = thisVm.$route.params.unique_id
      }
      const pokemonUrl = this.$constants('pokemonUrl')
      const cardSetsUrl = this.$constants('cardSetsUrl')
      const cardsUrl = this.$constants('cardsUrl')
      const cardUrl = `${cardsUrl}?unique_id=${encodeURI(thisVm.cardId)}`
      loadProgressBar()

      // get the cards data
      axios.get(cardUrl)
        .then(response => {
          if (response.data) {
            thisVm.status = response.status
            thisVm.card = response.data.results[0]
            thisVm.card.prices.map(price => {
              let cardUniqueId = utils.deepGet(thisVm.card, 'unique_id')
              price.card_unique_id = `${cardUniqueId}`
            })
            thisVm.numberInCardSet = response.data.results[0].number_in_set
          }
          // get the pokemon data linked to the card
          let pokemonId = response.data.results[0].pokemon
          return axios.get(`${pokemonUrl}${pokemonId}`)
        })
        .then(response => {
          thisVm.pokemon = response.data
          thisVm.pokemonId = response.data.id
          // get the card's set data
          const cardSetPath = `${cardSetsUrl}?code=${encodeURI(thisVm.card.card_set_code)}`
          return axios.get(cardSetPath)
        })
        .then(response => {
          thisVm.totalNoCardSet = response.data.results[0].total_cards
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
    },
    addCardToStorage (card) {
      let alreadySeenCards = []
      alreadySeenCards = JSON.parse(localStorage.getItem('seenCards'))
      if (!alreadySeenCards) {
        alreadySeenCards = []
        alreadySeenCards.push(card.unique_id)
        localStorage.setItem('seenCards', JSON.stringify(alreadySeenCards))
      } else {
        if (alreadySeenCards.some(seenCard => seenCard !== card.unique_id)) {
          alreadySeenCards.push(card.unique_id)
          localStorage.setItem('seenCards', JSON.stringify(alreadySeenCards))
        }
      }
    }
  },
  async mounted () {
    await this.getCardData()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-tooltip__content.copy-tooltip {
  border-radius: 0;
  padding: 2px 5px;
  font-size: 12px;
}
</style>
