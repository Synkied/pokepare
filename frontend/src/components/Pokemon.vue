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
                <p>{{ pokemon.name }}</p>
              </li>
            </ul>
            <p v-if="pokemon.cards.length === 1" class="mt-5">{{ pokemon.cards.length }} card found</p>
            <p v-else class="mt-5">{{ pokemon.cards.length }} card(s) found</p>
            <div class="row">
              <div class="col-xl-2 col-lg-3 col-md-4 col-xs-5 mt-3" v-for="card in pokemon.cards" :key="card.id">
                <li class="ns-li">
                  <a :href="card.url">
                    <img :src="card.image" height="250px" :alt="card.name">
                  </a>
                  <a :href="card.url">
                    <p>{{ card.name }}</p>
                  </a>
                </li>
              </div>
            </div>
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
import Sets from './Sets.vue'

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
      animated: false,
      errorMsg: null,
      cardSets: []
    }
  },
  title () {
    return `PokePare — ${this.pokemon}`
  },
  methods: {
  },
  components: {
    'sets': Sets
  },
  mounted () {
    var thisVm = this
    var cardSetsList = []
    if (thisVm.$route.params) {
      thisVm.pokemon_name = thisVm.$route.params.name
    }
    const path = '/api/pokemons/?name=' + capitalize(encodeURI(thisVm.pokemon_name))
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data.count > 0) {
        console.log(response.status)
        console.log(response.data)
        thisVm.pokemon = response.data.results[0]
        thisVm.status = response.status
        for (var i = 0; i < response.data.results[0].cards.length; i++) {
          cardSetsList.push(response.data.results[0].cards[i].card_set_code)
        }
        thisVm.cardSets = cardSetsList.filter(onlyUnique)
        // filter to get only unique values in array
      } else {
        thisVm.errorMsg = 'No Pokémon found.'
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
}
</script>

<!-- scoped styles for this component -->
<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

</style>
