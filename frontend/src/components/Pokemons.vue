<template>
  <div id="pokemons" class="container mt-5">
    <h2>{{ module_title }}</h2>
    <div>
      <template v-if="!user_query">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-4 col-lg-6 col-md-6 col-xs-1 mt-3"  v-for="pokemon in pokemons.slice(0, 12)" :key="pokemon.id">
              <ul>
                <li class="ns-li">
                  <a :href="pokemon.url"><img :src="pokemon.image" :alt="pokemon.name"></a>
                </li>
                <li class="ns-li">
                  <p><a :href="pokemon.url">{{ pokemon.name }}</a></p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </template>
      <template v-else-if="user_query && data_count > 0">
        <ul>
          <li class="ns-li" v-for="pokemon_name in pokemon_names" :key="pokemon_name.id">
            <a :href="pokemon.url">{{ pokemon_name }}</a>
          </li>
          <li class="ns-li" v-for="pokemon_img in pokemon_imgs" :key="pokemon_img.id">
            <img :src="pokemon_img" alt="">
          </li>
        </ul>
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
      data_count: null,
      status: '',
      pokemons: '',
      pokemon_names: [],
      pokemon_imgs: [],
      pokemon_cards: [],
      user_query: null,
      animated: false,
      error_msg: null,
      module_title: 'Pokemons'
    }
  },
  methods: {
    lookupGmapsWikiAPI () {
      var thisVm = this
      /* axios to ajax the query */
      if (thisVm.user_query) {
        const path = '/api/pokemons/?name=' + capitalize(encodeURI(thisVm.user_query))
        loadProgressBar()
        axios.get(path).then(response => {
          thisVm.data_count = response.data.count
          if (response.data) {
            console.log(response.data) // ex.: { user: 'Your User'}
            console.log(response.status) // ex.: 200
            thisVm.status = response.status
            thisVm.pokemon_names = [] // reset lists
            thisVm.pokemon_imgs = []
            for (var i = 0; i < response.data.results.length; i++) {
              thisVm.pokemon_names.push(capitalize(response.data.results[i].name))
              thisVm.pokemon_imgs.push(response.data.results[i].front_image)
              thisVm.pokemon_cards.push(response.data.results[i].cards)
            }
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
    const path = '/api/pokemons/'
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        console.log(response.data)
        thisVm.pokemons = response.data.results
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
