<template>
  <v-container id="search-bar">
    <v-text-field
      hide-details
      @keyup.esc="query=''"
      @keyup.enter="searchCards()"
      v-model="query"
      name="query"
      type="text"
      class="search-query"
      placeholder="Enter a Pokémon card name"
      append-icon="search"
      @click:append="searchCards()"
    />
  </v-container>
</template>

<script>

export default {
  name: 'SearchBar',
  data () {
    return {
      query: ''
    }
  },
  methods: {
    searchCards () {
      var thisVm = this
      if (window.location !== '/search/?query=') {
        window.location.href = ('/search/?query=') + thisVm.query
      }
    }
  }
}

</script>

<!-- scoped styles for this component -->
<style scoped>

</style>
