<template>
  <div id="cards">
    <div>
      <template v-if="card">
        <div class="container-fluid">
            <ul>
              <h3 class="card-title">{{ card.name }} - <a :href="'/sets/' + card.card_set_code">{{ card.card_set }}</a>
                <small>{{ uniqueNumInSet }}</small>
              </h3>
              <li class="ns-li">
                <img :src="card.image" :alt="card.name">
              </li>
            </ul>
            <small>
              <a :href="pokemon.url">
                <img :src="pokemon.image" alt="">
              </a>
            </small>

            <template v-if="card.prices.ebay">
              <div style="overflow-x:auto;">
                <table>
                  <thead>
                    <th>Website</th>
                    <th>Title</th>
                    <th>Condition</th>
                    <th>URL</th>
                    <th>Ships to</th>
                    <th>Current Price</th>
                    <th>Currency</th>
                  </thead>
                  <tr v-for="item in orderedPrices" :key="item.id">
                    <td>eBay</td>
                    <td>{{ item.title }}</td>
                    <td>{{ item.condition.conditionDisplayName }}</td>
                    <td><a :href="item.viewItemURL">{{ item.viewItemURL }}</a></td>
                    <td>{{ item.shippingInfo.shipToLocations }}</td>
                    <td>{{ item.sellingStatus.convertedCurrentPrice.value }}</td>
                    <td>{{ item.sellingStatus.convertedCurrentPrice._currencyId }}</td>
                  </tr>
                </table>
              </div>
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
      uniqueNumInSet: ''
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
            console.log(thisVm.pokemonId)
          })

          // get the card's set data
          const setPath = '/api/sets/?code=' + encodeURI(thisVm.card.card_set_code)
          axios.get(setPath).then(response => {
            thisVm.totalNoSet = response.data.results[0].total_cards
            thisVm.uniqueNumInSet = String(thisVm.numberInSet) + '/' + String(thisVm.totalNoSet)
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
