<template>
  <div id="cards">
    <div>
      <template v-if="card">
        <div class="container-fluid">
            <ul>
              <li class="ns-li">
                <img :src="card.image" :alt="card.name">
              </li>
            </ul>
            <li class="ns-li">
              <p>{{ card.name }}</p>
              <p>Number in set: {{ uniqueNumInSet }}</p>
              <p>Unique id: {{ card.unique_id }}</p>
            </li>
            <li class="ns-li">
              <h5>Found in this set:</h5>
              <p><a :href="'/sets/' + card.card_set_code">{{ card.card_set }}</a></p>
            </li>
            <li class="ns-li mt-5">
              <h4>Related Pokémon</h4>
              <a :href="pokemon.url">
                <img :src="pokemon.image" alt="">
              </a>
                <p><a :href="pokemon.url">{{ pokemon.name }}</a></p>
            </li>
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
      pokemon: '',
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
      axios.get(cardPath).then(response => {
        if (response.data) {
          thisVm.status = response.status
          thisVm.card = response.data.results[0]
          thisVm.numberInSet = response.data.results[0].number_in_set
          axios.get(response.data.results[0].pokemon).then(response => {
            thisVm.pokemon = response.data
          })

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
    }
  },
  components: {
  },
  mounted () {
    this.getCardData()
    console.log(this.uniqueNumInSet)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
