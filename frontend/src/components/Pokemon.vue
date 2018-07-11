<template>
  <div id="pokemons" class="container">
    <div>
      <template v-if="!user_query">
        <div class="container-fluid">
          <div v-for="pokemon in pokemons.slice(0, 12)" :key="pokemon.id">
            <ul>
              <li class="ns-li">
                <img :src="pokemon.image" :alt="pokemon.name">
              </li>
              <li class="ns-li">
                <p>{{ pokemon.name }}</p>
              </li>
            </ul>
            <p class="mt-5">{{ pokemon.cards.length }} card(s) found</p>
            <div class="row">
              <div class="col-xl-2 col-lg-3 col-md-4 col-xs-5 mt-3" v-for="card in pokemon.cards" :key="card.id">
                <li class="ns-li">
                  <a :href="card.url">
                    <img :src="card.image" height="250px" :alt="card.name">
                  </a>
                  <a :href="card.url">
                    <p>{{ card.name }}</p>
                  </a>
                </li>
              </div>
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
      user_query: null,
      animated: false,
      error_msg: null
    }
  },
  methods: {
  },
  components: {
    'rise-loader': RiseLoader
  },
  mounted () {
    var thisVm = this
    if (thisVm.$route.params) {
      thisVm.pokemon_name = thisVm.$route.params.name
    }
    const path = '/api/pokemons/?name=' + capitalize(encodeURI(thisVm.pokemon_name))
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        console.log(response.data.results)
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

</style>
