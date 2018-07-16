<template>
  <div id="sets">
    <div>
      <template>
        <div class="container-fluid">
            <ul>
              <li class="ns-li">
                <img :src="card_set.image" height="100px" :alt="card_set.name">
              </li>
            </ul>
            <li class="ns-li">
              <p>{{ card_set.name }}</p>
            </li>
            <li class="ns-li" v-if="set_code">
              <h5>Cards in this set:</h5>
              <cards :setCode="set_code"></cards>
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
      card_set: '',
      dataCount: null,
      errorMsg: null,
      set_code: ''
    }
  },
  components: {
    'cards': Cards
  },
  methods: {
    showCards () {
      var thisVm = this
      if (thisVm.$route.params) {
        thisVm.set_code = thisVm.$route.params.code
      }
      const setPath = '/api/sets/?code=' + encodeURI(thisVm.set_code)
      loadProgressBar()
      axios.get(setPath).then(response => {
        if (response.data) {
          console.log('sets status:', response.status)
          thisVm.status = response.status
          thisVm.card_set = response.data.results[0]
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
