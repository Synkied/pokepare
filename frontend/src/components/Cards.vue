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
      <template v-if="status === 200 && user_query == null">
        <p>{{ cards }}</p>
      </template>
      <template v-if="status === 200 && user_query != null">
        <p v-html="card_name" class="mt-1 card-text text-center"></p>
        <p v-html="card_desc" class="mt-1 card-text text-center"></p>
        <img :src="card_img" alt="card image">
      </template>
      <template v-else-if="status === 'NO_QUERY'">
        <p>Please enter a correct query.</p>
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
      status: '',
      cards: '',
      card_name: '',
      card_desc: '',
      card_img: '',
      user_query: null,
      msg: 'PokePare',
      animated: false
    }
  },
  methods: {
    lookupGmapsWikiAPI () {
      var thisVm = this
      /* axios to ajax the query */
      if (thisVm.user_query) {
        const path = '/api/cards/' + capitalize(encodeURI(thisVm.user_query))
        loadProgressBar()
        axios.get(path).then(response => {
          if (response.data) {
            console.log(response.data) // ex.: { user: 'Your User'}
            console.log(response.status)
            thisVm.card_name = capitalize(response.data.name)
            thisVm.card_desc = capitalize(response.data.description)
            thisVm.card_img = response.data.image
            thisVm.status = response.status
          }
        })
          .catch(function (error) {
            console.log(error)
          })
      } else {
        thisVm.status = 'NO_QUERY'
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
