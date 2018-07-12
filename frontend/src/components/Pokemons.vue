<template>
  <div id="pokemons" class="container mt-5">
    <h2>{{ module_title }}</h2>
    <h4>{{ data_count }} Pokemons</h4>
    <div>
      <template v-if="!user_query">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-2 col-lg-6 col-md-6 col-xs-1 mt-3"  v-for="pokemon in paginatedData" :key="pokemon.id">
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
          <button class="btn btn-info mt-5" :disabled="page_number === 0" @click="prevPage">Prev</button>
          <button class="btn btn-info mt-5" :disabled="page_number >= pageCount -1" @click="nextPage">Next</button>
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
      data_count: null,
      page_count: null,
      status: '',
      user_query: null,
      animated: false,
      error_msg: null,
      module_title: 'Pokemons',
      next_page: '',
      previous_page: '',
      page_number: 0
    }
  },
  props: {
    pokemons: {
      type: Array,
      required: true
    },
    size: {
      type: Number,
      required: false,
      default: 60
    }
  },
  computed: {
    pageCount () {
      let l = this.data_count.length
      let s = this.size
      return Math.floor(l / s)
    },
    paginatedData () {
      const start = this.page_number * this.size
      const end = start + this.size
      return this.pokemons.slice(start, end)
    }
  },
  methods: {
  /* viewMore () {
      axios.get(this.next_page).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.next_page = response.data.next
      })
    }, */
    nextPage () {
      axios.get(this.next_page).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.next_page = response.data.next
      })
      this.page_number++
    },
    prevPage () {
      axios.get(this.previous_page).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          this.pokemons.push(response.data.results[i])
        }
        this.previous_page = response.data.previous
      })
      this.page_number--
    }
  },
  components: {
  },
  mounted () {
    const path = '/api/pokemons/'
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        this.next_page = response.data.next
        this.pokemons = response.data.results
        this.data_count = response.data.count
        this.status = response.status
        console.log(response.data)
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
