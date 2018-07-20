<template>
  <div id="home" class="container">
    or upload an image file:
    <file-upload></file-upload>
    <h2 class="mt-5">What's PokePare?</h2>
    <img class="mb-4" src="../assets/pokepare_200.png" height="40px" alt="">
    <p>PokePare is all about finding the prices for Pokemon cards.</p>
    <p>It's also a bit more, as it has an API built-in to retrieve Pokemons, their cards, and the cards' sets. It is available at: <a href="http://pokepare.com/api/">pokepare.com/api/</a>.</p>
    <p>Some documentation will be written soon.</p>
    <p>The Pokemon' data and cards were built using (a big thank to them!):</p>
    <ul>
      <li class="ns-li"><a href="https://pokeapi.co/">Pokéapi</a></li>
      <li class="ns-li"><a href="http://pokemontcg.io/">PokemonTCG</a></li>
    </ul>
  </div>
</template>

<script>
/* Imports */
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import SearchBar from './SearchBar'
import Pokemons from './Pokemons'
import Cards from './Cards'
import FileUpload from './FileUpload.vue'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      moduleTitle: 'Home'
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  methods: {
  },
  components: {
    'rise-loader': RiseLoader,
    'search-bar': SearchBar,
    'pokemons': Pokemons,
    'cards': Cards,
    'file-upload': FileUpload
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
