<template>
  <div id="cards">
    <div>
      <template v-if="card">
        <div class="container-fluid">
            <ul>
              <li class="ns-li">
                <img :src="card.image" :alt="card.name">
              </li>
            </ul>
            <li class="ns-li">
              <p>{{ card.name }}</p>
            </li>
            <li class="ns-li">
              <h5>Found in this set:</h5>
              <p><a :href="'/sets/' + card.card_set_code">{{ card.card_set }}</a></p>
            </li>
            <li class="ns-li mt-5">
              <h4>Related Pokémon</h4>
              <a :href="pokemon.url">
                <img :src="pokemon.image" alt="">
              </a>
                <p><a :href="pokemon.url">{{ pokemon.name }}</a></p>
            </li>
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
      data: null,
      status: '',
      card: '',
      pokemon: '',
      errorMsg: null
    }
  },
  components: {
  },
  mounted () {
    var thisVm = this
    if (thisVm.$route.params) {
      thisVm.card_id = thisVm.$route.params.unique_id
    }
    const path = '/api/cards/?unique_id=' + encodeURI(thisVm.card_id)
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        thisVm.status = response.status
        thisVm.card = response.data.results[0]
        axios.get(response.data.results[0].pokemon).then(response => {
          thisVm.pokemon = response.data
        })
      }
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
