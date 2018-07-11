<template>
  <div id="pokemons" class="container mt-5">
    <h2>{{ module_title }}</h2>
    <h4>{{ data_count }} Pokemons</h4>
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
    </div>
  </div>
</template>

<script>
/* Imports */
import axios from 'axios'
import RiseLoader from 'vue-spinner/src/RiseLoader.vue'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      data_count: null,
      status: '',
      pokemons: '',
      user_query: null,
      animated: false,
      error_msg: null,
      module_title: 'Pokemons'
    }
  },
  methods: {
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
        thisVm.data_count = response.data.count
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
