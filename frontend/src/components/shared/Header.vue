<!-- Header file, used to define the navbar -->
<!--  Quentin Lathiere - synkx@hotmail.fr -->

<template>
  <div>
    <v-app-bar
      dark
      flat
      app
    >
      <router-link class="d-flex align-center white--text" :to="{ name: 'home' }">
        <img src="../../assets/pokepare_200.png" height="50" alt=""/>
        <span class="headline ml-1">POKÉPARE</span>
      </router-link>
      <v-spacer></v-spacer>
      <v-container id="app-bar-search-bar">
        <search-bar></search-bar>
      </v-container>
      <v-btn text small :to="{ name: 'allCards' }">Cards</v-btn>
      <v-btn text small :to="{ name: 'allPokemons', query: { page: 1, 'per_page': 60 } }">Pokémon</v-btn>
      <v-btn text small :to="{ name: 'allCardSets' }">Cards Sets</v-btn>
      <v-btn icon small to="#">
        <v-icon>
          face
        </v-icon>
      </v-btn>
<!--       <v-select
        v-model="selectedLanguage"
        :items="availableLanguages"
        dense
        flat
        solo
        item-value="iso639"
        prepend-inner-icon="translate"
        hide-details
        class="pl-1 pb-1 language-selection"
        @change="setUserLanguageInStores()"
      >
        <template v-slot:selection="{ item, index }">
          <span>
            {{ item.local_name }}
          </span>
        </template>
        <template v-slot:item="{ item, index }">
          <span>
            {{ item.local_name }}
          </span>
          <v-spacer>
          </v-spacer>
          <img :src="item.sprite"/>
        </template>
      </v-select> -->
      <v-menu>
        <template v-slot:activator="{ on }">
          <v-btn
            small
            dark
            text
            v-on="on"
          >
            <v-icon small left>translate</v-icon>
            {{ displayLanguage }}
            <v-icon small right>arrow_drop_down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            class="custom-list-item"
            v-for="(item, index) in availableLanguages"
            :key="index"
            @click="selectedLanguage = item.name; displayLanguage = item.local_name"
            @change="setUserLanguageInStores()"
          >
            <v-list-item-title class="v-list-item v-list-item--link custom-list-item-title">
              <span>{{ item.local_name }} </span> <span class="language-name">({{ item.name }})</span>
              <v-spacer></v-spacer>
              <img :src="item.sprite"/>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
import SearchBar from '../SearchBar'
import axios from 'axios'
import { mapMutations } from 'vuex'

export default {
  name: 'Header',
  components: {
    'search-bar': SearchBar
  },
  data () {
    return {
      selectedLanguage: '',
      displayLanguage: 'English',
      availableLanguages: []
    }
  },
  computed: {
  },
  methods: {
    ...mapMutations([
      'setUserLanguage'
    ]),
    setUserLanguageInStores () {
      localStorage.setItem('userLanguage', this.selectedLanguage)
      localStorage.setItem('displayLanguage', this.displayLanguage)
      this.setUserLanguage(this.selectedLanguage)
    },
    async getLanguages () {
      const languagesUrl = this.$constants('languagesUrl')
      try {
        let response = await axios.get(languagesUrl)
        let languages = response.data.results
        let languagesToAvoid = ['cs', 'pt-BR', 'ja-Hrkt', 'roomaji']
        for (var i = languages.length - 1; i >= 0; i--) {
          if (languagesToAvoid.includes(languages[i].name)) {
            languages.splice(i, 1)
          }
        }
        this.availableLanguages = languages.sort((a, b) => (a.name > b.name) ? 1 : -1)
      } catch (error) {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error(error.response.data)
          console.error(error.response.status)
          console.error(error.response.headers)
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser
          // and an instance of http.ClientRequest in node.js
          console.error(error.request)
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error', error.message)
        }
        console.error(error.config)
      }
    }
  },
  async mounted () {
    await this.getLanguages()
    this.selectedLanguage = localStorage.getItem('userLanguage')
    this.displayLanguage = localStorage.getItem('displayLanguage')
  }
}
</script>

<style>
.container#app-bar-search-bar {
  max-width: 500px;
}
.language-selection.v-input {
  max-width: 8%;
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
.v-list-item.v-list-item--link.custom-list-item-title {
  padding: 0 5px;
}
.custom-list-item .v-list-item, .custom-list-item.v-list-item {
  min-height: 28px !important;
}
.language-name {
  font-size: 11px;
  padding: 0 3px;
}
</style>
