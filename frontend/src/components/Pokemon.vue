<template>
  <div id="pokemons" class="container">
    <div>
      <template v-if="pokemon">
        <div class="container-fluid">
            <ul>
              <li class="ns-li">
                <img :src="pokemon.image" :alt="pokemon.name">
              </li>
              <li class="ns-li">
                <p v-if="pokemon.number < 10">#00{{ pokemon.number }}</p>
                <p v-else-if="pokemon.number < 100">#0{{ pokemon.number }}</p>
                <p v-else>#{{ pokemon.number }}</p>
                <p>{{ pokemon.name }}</p>
              </li>
            </ul>
            <li class="ns-li" v-if="cards">
              <cards :cards="cards" :dataCount="cards.length"></cards>
            </li>
        </div>
      </template>
      <template v-else>
        {{ errorMsg }}
      </template>

    </div>
  </div>
</template>

<script>
/* Imports */
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
import CardSets from './CardSets.vue'
import Cards from './Cards.vue'

function capitalize (s) {
  return s && s[0].toUpperCase() + s.slice(1)
}

function onlyUnique (value, index, self) {
  return self.indexOf(value) === index
}

/* data, methods, components... declaration */
export default {
  data () {
    return {
      dataCount: null,
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
  },
  components: {
    'cardsets': CardSets,
    'cards': Cards
  },
  mounted () {
    var thisVm = this
    var cardSetsList = []
    if (thisVm.$route.params) {
      thisVm.pokemon_name = thisVm.$route.params.name
    }
    const pokemonUrl = `/api/pokemons/?name=${capitalize(encodeURI(thisVm.pokemon_name))}`
    let pokemonId
    loadProgressBar()
    axios.get(pokemonUrl)
      .then(response => {
        if (response.data.count > 0) {
          thisVm.pokemon = response.data.results[0]
          thisVm.status = response.status
          pokemonId = response.data.results[0].id
          // filter to get only unique values in array
        } else {
          thisVm.errorMsg = 'No Pokémon found.'
        }
        const pokemonCardsUrl = `/api/cards/?pokemon_id=${pokemonId}`
        return axios.get(pokemonCardsUrl)
      })
      .then(response => {
        console.log(response)
        thisVm.cards = response.data.results
        for (var i = 0; i < response.data.results.length; i++) {
          cardSetsList.push(response.data.results[i].card_set_code)
        }
        thisVm.cardSets = cardSetsList.filter(onlyUnique)
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
}
</script>

<!-- scoped styles for this component -->
<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

</style>
