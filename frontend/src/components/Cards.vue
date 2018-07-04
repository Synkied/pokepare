<template>
  <div id="cards">
    <h1>{{ msg }}</h1>
          <fieldset>
          <input :class="{'bounce animated': animated}" @animationend="animated = false"
            @keyup.esc="user_query=''" @keyup.enter="[lookupGmapsWikiAPI(), animate()]"
            v-model="user_query" name="user_query" type="text" class="form-control" placeholder="Enter a Pokemon name">
        <button @click="[lookupGmapsWikiAPI(), animate()]" class="btn mt-5 mb-5 query_btn">Envoyer</button>
      </fieldset>
    <div>
      <template v-if="!user_query">
        <p>{{ cards }}</p>
      </template>
      <template v-else-if="user_query && data > 0">
        <p v-html="card_name" class="mt-1 card-text text-center"></p>
        <p v-html="card_desc" class="mt-1 card-text text-center"></p>
        <img :src="card_img" alt="card image">
      </template>
      <template v-else>
        <p> {{ error_msg }}</p>
      </template>
    </div>
  </div>
</template>

<script>
/* Imports */
import axios from 'axios'
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

function capitalize (s) {
  return s && s[0].toUpperCase() + s.slice(1)
}

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
      msg: 'PokePare',
      animated: false,
      error_msg: null
    }
  },
  methods: {
    lookupGmapsWikiAPI () {
      var thisVm = this
      /* axios to ajax the query */
      if (thisVm.user_query) {
        const path = '/api/cards/?name=' + capitalize(encodeURI(thisVm.user_query))
        loadProgressBar()
        axios.get(path).then(response => {
          thisVm.data = response.data.length
          if (response.data.length > 0) {
            console.log(response.data) // ex.: { user: 'Your User'}
            console.log(response.status) // ex.: 200
            thisVm.card_name = capitalize(response.data[0].name)
            thisVm.card_desc = capitalize(response.data[0].description)
            thisVm.card_img = response.data[0].image
            thisVm.status = response.status
          } else {
            thisVm.error_msg = 'No result found for this query.'
          }
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
      } else {
        thisVm.status = 'NO_QUERY'
        thisVm.error_msg = 'Please enter a correct query.'
      }
    },
    animate () {
      var thisVm = this
      thisVm.animated = true
    }
  },
  components: {
    'rise-loader': RiseLoader
  },
  mounted () {
    var thisVm = this
    const path = '/api/cards/'
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        console.log(response.data)
        thisVm.cards = response.data
        thisVm.status = response.status
      }
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
