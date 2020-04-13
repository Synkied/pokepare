<template>
  <v-container>
    <file-upload class="mb-5"></file-upload>
    <li class="ns-li" v-if="previouslySeenCards.results.length">
      <cards :cards="previouslySeenCards" customCardTitle="PREVIOUSLY SEEN CARDS"></cards>
    </li>
  </v-container>
</template>

<script>
/* Imports */
import axios from 'axios'

import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import SearchBar from './SearchBar'
import Pokemons from './Pokemons'
import Cards from './Cards'
import FileUpload from './FileUpload.vue'

/* data, methods, components... declaration */
export default {
  components: {
    'rise-loader': RiseLoader,
    'search-bar': SearchBar,
    'pokemons': Pokemons,
    'cards': Cards,
    'file-upload': FileUpload
  },
  data () {
    return {
      moduleTitle: 'Home',
      previouslySeenCards: {
        count: 0,
        results: []
      }
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  methods: {
    async getCards (previouslySeenCards) {
      let cardsUrl = this.$constants('cardsUrl')
      let seenCards = []
      for (var i = 0; i < 6; i++) {
        let cardUrl = `${cardsUrl}?unique_id=${previouslySeenCards[i]}`
        let response = await axios(cardUrl)
        if (response.data.results) {
          seenCards.push(...response.data.results)
        }
      }
      return seenCards
    }
  },
  async mounted () {
    let localStorageCards = JSON.parse(localStorage.getItem('seenCards'))
    this.previouslySeenCards.results = await this.getCards(localStorageCards)
    this.previouslySeenCards.count = this.previouslySeenCards.results.length
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
