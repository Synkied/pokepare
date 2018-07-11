<template>
  <div id="cards" class="container mt-5">
    <h2>{{ module_title }}</h2>
    <h4>{{ cards.length }} cards</h4>
    <div>
      <template v-if="!user_query">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-12 mt-3"  v-for="card in cards.slice(0, 12)" :key="card.id">
              <ul>
                <li class="ns-li mb-2">
                  <a :href="card.url"><img class="card-img" :src="card.image" alt=""></a>
                </li>
                <li class="ns-li">
                  <p><a :href="card.url">{{ card.name }}</a></p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
/* Imports */
import axios from 'axios'
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import SearchBar from './SearchBar'
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
      user_query: null,
      animated: false,
      error_msg: null,
      module_title: 'Cards'
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
            thisVm.card_img = response.data[0].image_url
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
    'rise-loader': RiseLoader,
    'search-bar': SearchBar
  },
  mounted () {
    var thisVm = this
    const path = '/api/cards/'
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        console.log(response.data)
        thisVm.cards = response.data.results
        thisVm.status = response.status
      }
    })
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

  .container {
    max-width: 960px;
  }

</style>
