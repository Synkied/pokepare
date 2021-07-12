<template>
  <v-container id="search-bar">
    <v-autocomplete
      v-model="selectedItem"
      :items="pokemons"
      :search-input.sync="query"
      :loading="isLoading"
      clearable
      chips
      solo
      dense
      hide-details
      @keyup.esc="query=''"
      @keyup.enter="searchCards()"
      @change="searchCards()"
      name="query"
      class="search-query elevation-0"
      placeholder="Enter something"
      item-text="name"
      item-value="name"
      :no-filter="true"
    >
      <template v-slot:no-data>
        <v-list-item>
          <v-list-item-title>
            Search for your favorite
            <strong>Pokémon</strong>
          </v-list-item-title>
        </v-list-item>
      </template>
      <template v-slot:selection="{ attr, on, item, selected }">
        <v-chip
          v-bind="attr"
          :input-value="selected"
          color="#fff"
          class="black--text selected-pokemon-chip"
          v-on="on"
        >
          <img :src="item.front_sprite" class="selected-pokemon-img">
          <span v-text="titleize(item.local_name)"></span>
        </v-chip>
      </template>
      <template v-slot:append>
        <v-btn
          text
          @click="searchCards()">
            Go!
        </v-btn>
      </template>
      <template v-slot:item="data">
        <template v-if="typeof data.item !== 'object'">
          <v-list-item-content v-text="data.item"></v-list-item-content>
        </template>
        <template v-else>
          <v-list-item-avatar v-if="data.item.front_sprite">
            <img :src="data.item.front_sprite">
          </v-list-item-avatar>
          <v-list-item-avatar v-else>
            <img src="../assets/pokepare_200.png" class="no-img-card">
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title v-html="titleize(data.item.local_name)"></v-list-item-title>
            <v-list-item-subtitle v-html="data.item.number"></v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </template>
    </v-autocomplete>
  </v-container>
</template>

<script>
import axios from 'axios'
import { mapGetters } from 'vuex'

import utils from '@/utils'

export default {
  name: 'SearchBar',
  data () {
    return {
      isLoading: false,
      query: null,
      selectedItem: '',
      cards: [],
      pokemons: []
    }
  },
  watch: {
    query: {
      handler (newVal, oldVal) {
        this.liveSearch(newVal)
      }
    }
  },
  computed: {
    ...mapGetters([
      'getUserLanguage'
    ])
  },
  methods: {
    titleize: utils.titleize,
    searchCards () {
      if (this.$route.path !== `/search/`) {
        this.$router.push({ name: 'search', query: { query: this.selectedItem } })
      }
    },
    async liveSearch (userQuery) {
      if (userQuery) {
        // const searchCardUrl = `${this.$constants('cardsUrl')}?insensitive_name=${encodeURI(userQuery)}&limit=2000`
        const searchPokemonUrl = `${this.$constants('pokemonsUrl')}?insensitive_name=${encodeURI(userQuery)}&limit=2000&language=${this.getUserLanguage}`
        // const searchPokemonUrl = `${this.$constants('pokemonSpeciesUrl')}?insensitive_name=${encodeURI(userQuery)}&limit=2000`

        try {
          this.isLoading = true
          // let responseCards = await axios.get(searchCardUrl)
          let responsePokemon = await axios.get(searchPokemonUrl)

          // if (responseCards.data.count > 0) {
          //   this.cards = responseCards.data.results
          // } else {
          //   this.errorMsg = 'No card found for this query.'
          //   this.cards = []
          //   console.log(this.errorMsg)
          // }

          if (responsePokemon.data.count > 0) {
            this.pokemons = responsePokemon.data.results
          } else {
            this.errorMsg = 'No pokémon found for this query.'
            this.pokemons = []
            console.error(this.errorMsg)
          }
          this.isLoading = false
        } catch (err) {
          if (err.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error(err.response.data)
            console.error(err.response.status)
            console.error(err.response.headers)
          } else if (err.request) {
            // The request was made but no response was received
            // `err.request` is an instance of XMLHttpRequest in the browser
            // and an instance of http.ClientRequest in node.js
            console.error(err.request)
          } else {
            // Something happened in setting up the request that triggered an Error
            console.error('Error', err.message)
          }
          console.error(err.config)
        }
      } else {
        this.status = 'NO_QUERY'
        this.errorMsg = 'Please enter a correct query.'
      }
    }
  }
}

</script>

<!-- scoped styles for this component -->
<style scoped>
.selected-pokemon-img {
  height: 34px;
}
.selected-pokemon-chip {
  border-radius: 5px;
}
.no-img-card {
  height: 20px;
  width: 20px;
  border-radius: 0;
}
</style>
