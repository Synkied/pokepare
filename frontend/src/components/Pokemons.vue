<template>
  <div id="pokemons" class="container mt-5">
    <h2>{{ moduleTitle }}</h2>
    <h4 v-if="dataCount">{{ dataCount }} Pokémon</h4>
    <button ref="previous" class="btn btn-info mt-5" :disabled="pageNumber === 0 || disable" @click="prevPage">Prev</button>
    <button ref="next" class="btn btn-info mt-5" :disabled="pageNumber >= pageCount -1 || disable" @click="nextPage">Next</button>
    <div>
      <template v-if="!userQuery">
        <div class="container-fluid">
          <div class="row" v-if="pokemons">
            <div class="col-xl-2 col-lg-6 col-md-6 col-6 col-xs-6 mt-3" v-for="pokemon in paginatedData" :key="pokemon.id">
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
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      dataCount: '',
      status: '',
      userQuery: null,
      animated: false,
      errorMsg: null,
      moduleTitle: 'Pokémon',
      next: '',
      previous: '',
      pageNumber: 0,
      limit: '',
      pokemons: '',
      disable: false
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  props: {
    size: {
      type: Number,
      required: false,
      default: 60
    }
  },
  computed: {
    pageCount () {
      let l = this.dataCount
      let s = this.size
      return Math.ceil(l / s)
    },
    paginatedData () {
      const start = this.pageNumber * this.size
      const end = start + this.size
      return this.pokemons.slice(start, end)
    }
  },
  methods: {
  /* viewMore () {
      axios.get(this.next).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.next = response.data.next
      })
    }, */
    nextPage () {
      this.disable = true
      axios.get(this.next)
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            this.pokemons.push(response.data.results[i])
            this.disable = false
          }
          this.next = response.data.next
        })
      this.pageNumber++
      if (this.pokemons.length === this.dataCount) {
        this.disable = false
      }
    },
    prevPage () {
      axios.get(this.previous).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.previous = response.data.previous
      })
      this.pageNumber--
    }
  },
  components: {
  },
  mounted () {
    const pokemonUrl = this.$constants.pokemonURL
    loadProgressBar()
    axios.get(pokemonUrl).then(response => {
      if (response.data) {
        console.log(response.status)
        this.next = response.data.next
        this.pokemons = response.data.results
        this.dataCount = response.data.count
        this.status = response.status
        this.limit = Number(this.next.substring(this.next.indexOf('=') + 1, this.next.indexOf('&')))
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
