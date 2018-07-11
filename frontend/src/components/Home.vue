<template>
  <div id="home" class="container">
      <pokemons></pokemons>
      <cards></cards>
  </div>
</template>

<script>
/* Imports */
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import SearchBar from './SearchBar'
import Pokemons from './Pokemons'
import Cards from './Cards'

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
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

</style>
