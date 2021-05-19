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
import Cards from './Cards'
import FileUpload from './FileUpload.vue'

/* data, methods, components... declaration */
export default {
  components: {
    'cards': Cards,
    'file-upload': FileUpload
  },
  data () {
    return {
      moduleTitle: 'Home',
      previouslySeenCards: {
        results: []
      }
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  async mounted () {
    // trick to not load entire card
    let localStorageSeenCards = JSON.parse(localStorage.getItem('seenCards'))
    if (localStorageSeenCards.length) {
      let truncatedLocalStorageSeenCards = localStorageSeenCards.splice(0, 6)
      this.previouslySeenCards.results = truncatedLocalStorageSeenCards
    }
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
