<template>
  <div id="cards" class="container">
    <h1> {{ moduleTitle }}</h1>
    <div class="container-fluid" v-if="cards">
      <div class="row">
        <h4 class="col-xl-12 mb-3">{{ dataCount }} cards found</h4>
          <div class="col-xl-2 col-lg-2 col-md-3 col-sm-4 col-6 mt-3" v-for="card in cards" :key="card.id">
            <ul>
              <li class="ns-li mb-2">
                <a :href="card.url"><img class="card-img" :src="card.image" alt=""></a>
              </li>
              <li class="ns-li">
                <p ><a :href="card.url">{{ card.name }}</a></p>
              </li>
            </ul>
          </div>
      </div>
      <div v-if="nextPage">
        <button class="btn btn-info mt-5" @click="[viewMore()]">View more</button>
      </div>
    </div>
    <!-- Display error message if nothing found -->
    <div v-else>
      {{ errorMsg }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

export default {
  name: 'SearchBar',
  props: ['query'],
  data () {
    return {
      moduleTitle: 'Search',
      userQuery: '',
      status: null,
      cards: [],
      nextPage: '',
      dataCount: '',
      errorMsg: ''
    }
  },
  methods: {
    searchCards () {
      var thisVm = this
      /* axios to ajax the query */
      thisVm.userQuery = thisVm.$route.query.query
      if (thisVm.userQuery) {
        const path = '/api/cards/?insensitive_name=' + encodeURI(thisVm.userQuery)
        loadProgressBar()
        axios.get(path).then(response => {
          if (response.data.count > 0) {
            console.log('search_bar', response.data) // ex.: { user: 'Your User'}
            thisVm.cards = response.data.results
            thisVm.dataCount = response.data.count
            thisVm.status = response.status
            thisVm.nextPage = response.data.next
          } else {
            thisVm.errorMsg = 'No result found for this query.'
            thisVm.cards = ''
            console.log(thisVm.errorMsg)
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
        thisVm.errorMsg = 'Please enter a correct query.'
      }
    },
    viewMore () {
      var thisVm = this
      axios.get(thisVm.nextPage).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          thisVm.cards.push(response.data.results[i])
        }
        thisVm.nextPage = response.data.next
      })
    }
  },
  mounted () {
    var thisVm = this
    thisVm.searchCards()
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
