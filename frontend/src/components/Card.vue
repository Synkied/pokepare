<template>
  <div id="cards">
    <div>
      <template v-if="!user_query">
        <div class="container-fluid">
          <div v-for="card in cards.slice(0, 12)" :key="card.id">
            <ul>
              <li class="ns-li">
                <img :src="card.image" :alt="card.name">
              </li>

            </ul>
            <li class="ns-li">
              <p>{{ card.name }}</p>
            </li>
            <li class="ns-li">
              <p>{{ card.pokemon }}</p>
            </li>
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
      data: null,
      status: '',
      cards: '',
      error_msg: null
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
        console.log(response.data)
        thisVm.cards = response.data.results
        thisVm.status = response.status
      }
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
