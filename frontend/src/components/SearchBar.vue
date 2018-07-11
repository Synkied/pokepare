<template>
  <div id="cards" class="container">
    <h1> {{ module_title }}</h1>
    <fieldset>
        <input :class="{'bounce animated': animated}" @animationend="animated = false"
          @keyup.esc="user_query=''" @keyup.enter="[lookupGmapsWikiAPI(), animate()]"
          v-model="user_query" name="user_query" type="text" class="form-control" placeholder="Enter a Pokemon name">
      <button @click="[lookupGmapsWikiAPI(), animate()]" class="btn mt-5 mb-5 query_btn">Envoyer</button>
    </fieldset>
    <div>{{ cards }}</div>
  </div>
  </template>

<script>
import axios from 'axios'
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

function capitalize (s) {
  return s && s[0].toUpperCase() + s.slice(1)
}

export default {
  name: 'SearchBar',
  data () {
    return {
      module_title: 'Search a Card by name or image',
      user_query: null,
      animated: false,
      status: null,
      cards: ''
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
          if (response.data.length > 0) {
            console.log('search_bar', response.data) // ex.: { user: 'Your User'}
            console.log('search_bar', response.status) // ex.: 200
            thisVm.cards = response.data.results
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
  }
}

</script>

<!-- scoped styles for this component -->
<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

  .white-txt {
    color: #fff;
  }

  .query_btn{
    background-color: #2B7A78;
    color: #fff;
    font-family: 'Raleway', sans-serif;
    font-weight: bold;
  }

  .query_btn:hover{
    background-color: #55c3c0;
  }

  .animated {
    -webkit-animation-duration: 1s;
    animation-duration: 1s;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
  }

  .animated.infinite {
    -webkit-animation-iteration-count: infinite;
    animation-iteration-count: infinite;
  }

  .animated.hinge {
    -webkit-animation-duration: 2s;
    animation-duration: 2s;
  }

  .animated.flipOutX,
  .animated.flipOutY,
  .animated.bounceIn,
  .animated.bounceOut {
    -webkit-animation-duration: .75s;
    animation-duration: .75s;
  }

  @-webkit-keyframes bounce {
    from, 20%, 53%, 80%, to {
      -webkit-animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
      animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
      -webkit-transform: translate3d(0,0,0);
      transform: translate3d(0,0,0);
    }

    40%, 43% {
      -webkit-animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      -webkit-transform: translate3d(0, -30px, 0);
      transform: translate3d(0, -30px, 0);
    }

    70% {
      -webkit-animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      -webkit-transform: translate3d(0, -15px, 0);
      transform: translate3d(0, -15px, 0);
    }

    90% {
      -webkit-transform: translate3d(0,-4px,0);
      transform: translate3d(0,-4px,0);
    }
  }

  @keyframes bounce {
    from, 20%, 53%, 80%, to {
      -webkit-animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
      animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
      -webkit-transform: translate3d(0,0,0);
      transform: translate3d(0,0,0);
    }

    40%, 43% {
      -webkit-animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      -webkit-transform: translate3d(0, -30px, 0);
      transform: translate3d(0, -30px, 0);
    }

    70% {
      -webkit-animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      animation-timing-function: cubic-bezier(0.755, 0.050, 0.855, 0.060);
      -webkit-transform: translate3d(0, -15px, 0);
      transform: translate3d(0, -15px, 0);
    }

    90% {
      -webkit-transform: translate3d(0,-4px,0);
      transform: translate3d(0,-4px,0);
    }
  }

  .bounce {
    -webkit-animation-name: bounce;
    animation-name: bounce;
    -webkit-transform-origin: center bottom;
    transform-origin: center bottom;
  }
</style>
