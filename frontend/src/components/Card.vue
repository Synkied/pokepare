<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
          <fieldset>
          <input :class="{'bounce animated': animated}" @animationend="animated = false"
            @keyup.esc="user_query=''" @keyup.enter="[lookupGmapsWikiAPI(), animate()]"
            v-model="user_query" name="user_query" type="text" class="form-control" placeholder="Enter a Pokemon name">
        <button @click="[lookupGmapsWikiAPI(), animate()]" class="btn mt-5 mb-5 query_btn">Envoyer</button>
      </fieldset>
    <div>
      <template v-if="status === 200">
        <p v-html="card_name" class="mt-1 card-text text-center"></p>
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
      user_query: '',
      msg: 'test',
      card_name: '',
      status: '',
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
