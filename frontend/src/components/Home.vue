<template>
  <div id="home" class="container">
      <pokemons></pokemons>
      <cards></cards>
  </div>
</template>

<script>
/* Imports */
import axios from 'axios'
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import SearchBar from './SearchBar'
import Pokemons from './Pokemons'
import Cards from './Cards'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

function capitalize (s) {
  return s && s[0].toUpperCase() + s.slice(1)
}

/* data, methods, components... declaration */
export default {
  data () {
    return {
      data: null,
      status: '',
      cards: '',
      card_name: '',
      card_desc: '',
      card_img: '',
      user_query: null,
      animated: false,
      error_msg: null
    }
  },
  methods: {
  },
  components: {
    'rise-loader': RiseLoader,
    'search-bar': SearchBar,
    'pokemons': Pokemons,
    'cards': Cards
  },
  mounted () {
    var thisVm = this
    const path = '/api/cards/'
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        console.log(response.data)
        thisVm.cards = response.data.results
        thisVm.status = response.status
      }
    })
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

</style>
