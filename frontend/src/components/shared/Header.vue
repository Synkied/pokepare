<!-- Header file, used to define the navbar -->
<!--  Quentin Lathiere - synkx@hotmail.fr -->

<template>
  <div>
    <v-app-bar
      dark
      flat
      app
    >
      <a class="d-flex align-center white--text" href="/">
        <img src="../../assets/pokepare_200.png" height="50" alt=""/>
        <span class="headline ml-1">POKÉPARE</span>
      </a>
      <v-spacer></v-spacer>
      <v-container id="app-bar-search-bar">
        <search-bar></search-bar>
      </v-container>
      <v-btn text small to="/cards">Cards</v-btn>
      <v-btn text small to="/pokemons">Pokémon</v-btn>
      <v-btn text small to="/cardsets">Cards Sets</v-btn>
      <v-btn icon small to="#">
        <v-icon>
          face
        </v-icon>
      </v-btn>
      <v-select
        v-model="selectedLanguage"
        :items="availableLanguages"
        dense
        item-value="iso639"
        prepend-inner-icon="language"
        hide-details
        class="pb-1 language-selection"
        @change="setUserLanguageInStore()"
      >
        <template v-slot:selection="{ item, index }">
          <span>
            {{ item.iso639.toUpperCase() }}
          </span>
        </template>
        <template v-slot:item="{ item, index }">
          <span>
            {{ item.iso639.toUpperCase() }}
          </span>
          <v-spacer>
          </v-spacer>
          <img :src="item.sprite"/>
        </template>
      </v-select>
    </v-app-bar>
  </div>
</template>

<script>
import SearchBar from '../SearchBar'
import axios from 'axios'
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'Header',
  components: {
    'search-bar': SearchBar
  },
  data () {
    return {
      selectedLanguage: '',
      availableLanguages: []
    }
  },
  computed: {
    ...mapGetters([
      'getUserLanguage'
    ])
  },
  methods: {
    ...mapMutations([
      'setUserLanguage'
    ]),
    setUserLanguageInStore () {
      console.log(this.selectedLanguage)
      this.setUserLanguage(this.selectedLanguage)
    },
    async getLanguages () {
      const languagesUrl = this.$constants('languagesUrl')
      axios.get(languagesUrl)
        .then(response => {
          this.availableLanguages = response.data.results
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
  },
  async mounted () {
    await this.getLanguages()
    // this.selectedLanguage = this.getUserLanguage()
  }
}
</script>

<style>
.container#app-bar-search-bar {
  max-width: 500px;
}
.language-selection.v-input {
  max-width: 4.5%;
}
.v-list--dense .v-list-item {
  min-height: 28px !important;
}
.v-list--dense .v-list-item .v-list-item__content {
  padding: 0;
}
.v-text-field.v-input--dense:not(.v-text-field--enclosed):not(.v-text-field--full-width) .v-input__append-inner .v-input__icon > .v-icon, .v-text-field.v-input--dense:not(.v-text-field--enclosed):not(.v-text-field--full-width) .v-input__prepend-inner .v-input__icon > .v-icon {
  margin-top: 6px
}
</style>
