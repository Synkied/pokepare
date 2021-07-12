<template>
  <v-container id="search">
    <h1 class="display-2 white--text"> {{ moduleTitle }} <em>'{{ query }}'</em></h1>
    <div v-if="cards">
      <cards :cards="cards"></cards>
    </div>
    <!-- Display error message if nothing found -->
    <div v-else>
      {{ errorMsg }}
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import Cards from './Cards.vue'

export default {
  name: 'SearchBar',
  props: ['query'],
  data () {
    return {
      moduleTitle: 'Results for ',
      userQuery: '',
      status: null,
      cards: {},
      nextPage: '',
      dataCount: '',
      errorMsg: ''
    }
  },
  watch: {
    '$route.query.query': {
      handler (newVal, oldVal) {
        this.searchCards(newVal)
      }
    }
  },
  methods: {
    searchCards () {
      var thisVm = this
      /* axios to ajax the query */
      thisVm.userQuery = thisVm.$route.query.query || ''
      console.log(thisVm.userQuery)
      if (thisVm.userQuery) {
        const searchCardUrl = `${this.$constants('cardsUrl')}?insensitive_name=${encodeURI(thisVm.userQuery)}`
        axios.get(searchCardUrl).then(response => {
          console.log(response)
          if (response.data.count > 0) {
            thisVm.cards = response.data
          } else {
            thisVm.errorMsg = 'No result found for this query.'
            thisVm.cards = ''
            console.error(thisVm.errorMsg)
          }
        })
          .catch(function (error) {
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
          })
      } else {
        thisVm.status = 'NO_QUERY'
        thisVm.errorMsg = 'Please enter a correct query.'
      }
    }
  },
  mounted () {
    this.searchCards(this.$route.query.query)
  },
  components: {
    'cards': Cards
  }
}

</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
