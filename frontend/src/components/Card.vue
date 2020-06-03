<template>
  <div id="cards">
    <div>
      <v-container v-if="card">
        <v-card flat outlined>
          <v-card-title class="pokemon-title title justify-center">
            {{ card.name }}&nbsp;-&nbsp;
            <router-link :to="{ name: 'cardSetDetail', params: { code: card.card_set_code }}">{{ card.card_set }}</router-link>
            <v-tooltip content-class="card-number-in-set-title" right>
              <template v-slot:activator="{ on }">
                <small v-on="on">&nbsp;{{ card.number_in_set }}</small>
              </template>
              <span>Card number in set</span>
            </v-tooltip>
          </v-card-title>
          <img :src="card.image" :alt="card.name">
          <div class="mt-2 related-pokemon-image" v-if="pokemon">
            <router-link :to="{ name: 'pokemonDetail', params: { name: pokemon.name }}" class="pokemon-link">
              <img :src="pokemon.front_sprite" :alt="pokemon.local_name">
              <p>#{{ pokemon.number }}</p>
            </router-link>
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
import { mapGetters } from 'vuex'

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
    return `PokePare — ${utils.deepGet(this.card, 'name')}`
  },
  watch: {
    card: function (newCard, oldCard) {
      let cardToAddToLocalStorage = {}
      if (newCard) {
        cardToAddToLocalStorage.unique_id = newCard.unique_id
        cardToAddToLocalStorage.image = newCard.image
        cardToAddToLocalStorage.name = newCard.name
        utils.addObjectToLocalStorage('seenCards', cardToAddToLocalStorage, 'unique_id')
      }
    }
  },
  computed: {
    orderedPrices () {
      let sortedCardPrices = JSON.parse(JSON.stringify(this.card.prices))
      sortedCardPrices = sortedCardPrices.sort((a, b) => {
        return a.market_price - b.market_price
      })
      return sortedCardPrices
    },
    ...mapGetters([
      'getUserLanguage'
    ])
  },
  methods: {
    async getCardData () {
      var thisVm = this
      if (thisVm.$route.params) {
        thisVm.cardId = thisVm.$route.params.unique_id
      }
      const pokemonsUrl = this.$constants('pokemonsUrl')
      const cardSetsUrl = this.$constants('cardSetsUrl')
      const cardsUrl = this.$constants('cardsUrl')
      const cardDetailUrl = `${cardsUrl}?unique_id=${encodeURI(thisVm.cardId)}`
      loadProgressBar()

      // get the cards data
      axios.get(cardDetailUrl)
        .then(response => {
          if (response.data) {
            thisVm.status = response.status
            thisVm.card = response.data.results[0] || ''
            let cardPrices = utils.deepGet(thisVm.card, 'prices')
            if (cardPrices) {
              cardPrices.map(price => {
                let cardUniqueId = utils.deepGet(thisVm.card, 'unique_id')
                price.card_unique_id = `${cardUniqueId}`
              })
            }
            thisVm.numberInCardSet = response.data.results[0].number_in_set
          }
          // get the pokemon data linked to the card
          let pokemonId = response.data.results[0].pokemon
          return axios.get(`${pokemonsUrl}${pokemonId}?language=${this.getUserLanguage}`)
        })
        .then(response => {
          thisVm.pokemon = response.data
          thisVm.pokemonId = response.data.id
          // get the card's set data
          let cardSetCode = utils.deepGet(thisVm.card, 'card_set_code')
          const cardSetPath = `${cardSetsUrl}?code=${encodeURI(cardSetCode)}`
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

.pokemon-title small {
  font-size: 60%;
  color: #6f6f6f;
  line-height: 0;
}

.pokemon-title {
  font-family: 'Oswald', sans-serif;
  font-weight: 600;
}

.pokemon-title a {
  color: #0db4b9;
}

.v-tooltip__content.card-number-in-set-title {
  border-radius: 0;
  padding: 2px 5px;
  font-size: 11px;
}

</style>
