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
          <v-container fluid>
            <v-card>
              <v-data-table
                dark
                dense
                :headers="headers"
                :items="orderedPrices"
                :options="tableOptions"
              >
              <template v-slot:top>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field
                        v-model="searchQuery"
                        dense
                        label="Search"
                      ></v-text-field>
                    </v-col>
                    <v-col>
                      <v-autocomplete
                        v-model="values"
                        :items="items"
                        dense
                        chips
                        small-chips
                        label="Website"
                        multiple
                      ></v-autocomplete>
                    </v-col>
                    <v-col>
                      <v-autocomplete
                        v-model="values"
                        :items="items"
                        dense
                        chips
                        small-chips
                        label="Condition"
                        multiple
                      ></v-autocomplete>
                    </v-col>
                    <v-col>
                      <v-autocomplete
                        v-model="values"
                        :items="items"
                        dense
                        chips
                        small-chips
                        label="Edition"
                        multiple
                      ></v-autocomplete>
                    </v-col>
                    <v-col>
                      <v-autocomplete
                        v-model="values"
                        :items="items"
                        dense
                        chips
                        small-chips
                        label="Currency"
                        multiple
                      ></v-autocomplete>
                    </v-col>
                  </v-row>
                </v-container>
              </template>
              <template v-slot:item.link="{ item }">
                <v-btn icon color="primary" :to="item.link">
                  <v-icon small>
                    launch
                  </v-icon>
                </v-btn>
              </template>
              <template v-slot:item.copy_row="{ item }">
                <v-btn icon color="secondary" @click="copyRow(item.product_id)">
                  <v-icon small>
                    file_copy
                  </v-icon>
                </v-btn>
              </template>
              </v-data-table>
            </v-card>
          </v-container>
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

/* data, methods, components... declaration */
export default {
  data () {
    return {
      headers: [
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
      values: ''
    }
  },
  title () {
    return `PokePare — ${this.card.name}`
  },
  methods: {
    getCardData () {
      var thisVm = this
      if (thisVm.$route.params) {
        thisVm.cardId = thisVm.$route.params.unique_id
      }
      const pokemonURL = this.$constants('pokemonURL')
      const cardSetsURL = this.$constants('cardSetsURL')
      const cardsURL = this.$constants('cardsURL')
      const cardURL = `${cardsURL}?unique_id=${encodeURI(thisVm.cardId)}`
      loadProgressBar()

      // get the cards data
      axios.get(cardURL)
        .then(response => {
          if (response.data) {
            thisVm.status = response.status
            thisVm.card = response.data.results[0]
            thisVm.numberInCardSet = response.data.results[0].number_in_set
          }
          // get the pokemon data linked to the card
          let pokemonId = response.data.results[0].pokemon
          return axios.get(`${pokemonURL}${pokemonId}`)
        })
        .then(response => {
          thisVm.pokemon = response.data
          thisVm.pokemonId = response.data.id
          // get the card's set data
          const cardSetPath = `${cardSetsURL}?code=${encodeURI(thisVm.card.card_set_code)}`
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
    copyRow (productId) {
      for (var i = this.card.prices.length - 1; i >= 0; i--) {
        if (this.card.prices[i].product_id === productId) {
          this.$clipboard(this.card.prices[i])
        }
      }
    }
  },
  computed: {
    orderedPrices () {
      let sortedCardPrices = JSON.parse(JSON.stringify(this.card.prices))
      return sortedCardPrices.sort((a, b) => {
        return a.market_price - b.market_price
      })
    }
  },
  mounted () {
    this.getCardData()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
