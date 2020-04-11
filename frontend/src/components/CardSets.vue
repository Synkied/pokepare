<template>
  <v-container id="cardsets">
    <v-card flat outlined>
      <v-card-title>
        {{ dataCount }} card sets
      </v-card-title>
      <div>
        <v-row v-if="cardSets">
          <v-col
            cols="12"
            md="2"
            v-for="cardSet in cardSets"
            :key="cardSet.id">
            <ul>
              <li class="ns-li mb-2">
                <a :href="cardSet.url">
                  <img class="cardset-img" :src="cardSet.image" height="25px" :alt="cardSet.name">
                </a>
              </li>
              <li class="ns-li">
                <p><a :href="cardSet.url">{{ cardSet.name }}</a></p>
              </li>
            </ul>
          </v-col>
            <div v-if="next">
              <button class="btn btn-info mt-5" @click="[viewMore()]">View more</button>
            </div>
        </v-row>
      </div>
    </v-card>
  </v-container>
</template>

<script>
/* Imports */
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

/* data, methods, components... declaration */
export default {
  props: ['cardSetCodes'],
  data () {
    return {
      dataCount: null,
      pageCount: null,
      status: '',
      cardSets: [],
      animated: false,
      errorMsg: null,
      moduleTitle: 'Card sets',
      next: '',
      cardSetCodesValues: this.cardSetCodes
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  methods: {
    viewMore () {
      var thisVm = this
      axios.get(thisVm.next).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          thisVm.cardSets.push(response.data.results[i])
        }
        thisVm.next = response.data.next
      })
    },
    viewSets () {
      var thisVm = this
      loadProgressBar()
      let cardSetsURL = this.$constants('cardSetsURL')
      axios.get(cardSetsURL).then(response => {
        if (response.data) {
          console.log(response.status)
          console.log(response.data)
          thisVm.cardSets = response.data.results
          thisVm.status = response.status
          thisVm.dataCount = response.data.count
          thisVm.next = response.data.next
        }
      })
    }
  },
  components: {
  },
  mounted () {
    var thisVm = this
    thisVm.viewSets()
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
