<template>
  <v-container>
    <file-upload class="mb-5"></file-upload>
  </v-container>
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
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
