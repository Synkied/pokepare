<template>
  <div id="cards">
    <div>
      <template v-if="card">
        <div class="container">
            <ul>
              <h3 class="card-title">{{ card.name }} - <a :href="'/sets/' + card.card_set_code">{{ card.card_set }}</a>
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
            <template v-if="card.prices">
              <template v-if="card.prices.ebay || card.prices.tcgplayer">
                <div style="overflow-x:auto;">
                  <table width="100%">
                    <thead>
                      <th>Website</th>
                      <th>Condition</th>
                      <th>Edition</th>
                      <th>URL</th>
                      <th>Current Price</th>
                      <th>Currency</th>
                    </thead>
                    <tbody>
                      <tr v-for="item in orderedPrices" :key="item.id">
                        <td>eBay</td>
                        <td>{{ item.condition.conditionDisplayName }}</td>
                        <td>N/A</td>
                        <td><a :href="item.viewItemURL">{{ item.viewItemURL }}</a></td>
                        <td id="price">{{ item.sellingStatus.convertedCurrentPrice.value }}</td>
                        <td>{{ item.sellingStatus.convertedCurrentPrice._currencyId }}</td>
                      </tr>
                    </tbody>
                    <tbody v-if="card.prices.tcgplayer" v-for="item in card.prices.tcgplayer" :key="item.id">
                      <tr v-for="price in item.prices" :key="price.id">
                        <td>TCGPlayer</td>
                        <td>N/A</td>
                        <td>{{ price.subTypeName }}</td>
                        <td><a :href="item.viewItemURL">{{ item.viewItemURL }}</a></td>
                        <td id="price">{{ price.marketPrice }}</td>
                        <td>USD</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </template>
            </template>
            <template v-else>
              <p>No prices found for this card.</p>
            </template>
        </div>
      </template>
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
      data: null,
      status: '',
      card: '',
      cardId: '',
      prevPokemon: '',
      pokemon: '',
      pokemonId: '',
      nextPokemon: '',
      errorMsg: null,
      numberInSet: '',
      totalNoSet: '',
      uniqueNumInSet: '',
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
      const cardPath = '/api/cards/?unique_id=' + encodeURI(thisVm.cardId)
      loadProgressBar()

      // get the cards data
      axios.get(cardPath).then(response => {
        if (response.data) {
          thisVm.status = response.status
          thisVm.card = response.data.results[0]
          thisVm.numberInSet = response.data.results[0].number_in_set

          // get the pokemon data linked to the card
          axios.get(response.data.results[0].pokemon).then(response => {
            thisVm.pokemon = response.data
            thisVm.pokemonId = response.data.id
          })

          // get the card's set data
          const setPath = '/api/sets/?code=' + encodeURI(thisVm.card.card_set_code)
          axios.get(setPath).then(response => {
            thisVm.totalNoSet = response.data.results[0].total_cards
            /* thisVm.uniqueNumInSet = String(thisVm.numberInSet) + '/' + String(thisVm.totalNoSet) */
          })
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
    _ToggleNext () {
      if (this.pokemonId === this.numOfPokemon - 1) {
        return
      }
      this.setState(prevState => ({
        selectedIndex: prevState.selectedIndex + 1
      }))
    }
  },
  computed: {
    orderedPrices () {
      return this.lodash.orderBy(this.card.prices.ebay, 'sellingStatus.convertedCurrentPrice.value')
    }
  },
  components: {
  },
  mounted () {
    this.getCardData()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
