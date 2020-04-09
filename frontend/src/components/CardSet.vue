<template>
  <div id="sets">
    <div>
      <template>
        <div class="container-fluid">
            <ul>
              <li class="ns-li">
                <img :src="cardSet.image" height="100px" :alt="cardSet.name">
              </li>
            </ul>
            <li class="ns-li">
              <p>{{ cardSet.name }}</p>
            </li>
            <li class="ns-li" v-if="cardSetCode">
              <cards :cardSetCode="cardSetCode"></cards>
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
import Cards from './Cards.vue'

/* data, methods, components... declaration */
export default {
  data () {
    return {
      data: null,
      status: '',
      cardSet: '',
      dataCount: null,
      errorMsg: null,
      cardSetCode: ''
    }
  },
  title () {
    return `PokePare — ${this.cardSetCode}`
  },
  components: {
    'cards': Cards
  },
  methods: {
    showCards () {
      var thisVm = this
      if (thisVm.$route.params) {
        thisVm.cardSetCode = thisVm.$route.params.code
      }
      const cardSetURL = `${this.$constants('cardSetsURL')}?code=${encodeURI(thisVm.cardSetCode)}`
      loadProgressBar()
      console.log(cardSetURL)
      axios.get(cardSetURL).then(response => {
        console.log(response)
        if (response.data) {
          thisVm.status = response.status
          thisVm.cardSet = response.data.results[0]
        }
      })
    }
  },
  mounted () {
    var thisVm = this
    thisVm.showCards()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
