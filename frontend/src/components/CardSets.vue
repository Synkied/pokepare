<template>
  <v-container id="cardsets">
    <v-card tile flat outlined>
      <v-card-title class="secondary darken-1 headline">
        {{ dataCount }} CARD SETS
      </v-card-title>
      <v-divider class="mb-5"></v-divider>
      <div>
        <v-row v-if="cardSets">
          <v-col
            cols="4"
            md="2"
            v-for="cardSet in cardSets"
            :key="cardSet.id">
            <ul class="mb-5">
              <li class="ns-li mb-2">
                <router-link :to="{ name: 'cardSetDetail', params: { code: cardSet.code }}">
                  <img class="cardset-img" :src="cardSet.image" :alt="cardSet.name">
                </router-link>
              </li>
              <li class="ns-li">
                <p>
                  <router-link :to="{ name: 'cardSetDetail', params: { code: cardSet.code }}">
                    {{ cardSet.name }}
                  </router-link>
                </p>
              </li>
            </ul>
          </v-col>
        </v-row>
      </div>
      <div v-if="nextPage">
        <v-btn
          class="my-5"
          @click="viewMore()">
            View more
        </v-btn>
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
      nextPage: '',
      cardSetCodesValues: this.cardSetCodes
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  methods: {
    viewMore () {
      var thisVm = this
      axios.get(thisVm.nextPage).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          thisVm.cardSets.push(response.data.results[i])
        }
        thisVm.nextPage = response.data.next
      })
    },
    viewSets () {
      var thisVm = this
      loadProgressBar()
      let cardSetsUrl = this.$constants('cardSetsUrl')
      axios.get(cardSetsUrl).then(response => {
        if (response.data) {
          thisVm.cardSets = response.data.results
          thisVm.status = response.status
          thisVm.dataCount = response.data.count
          thisVm.nextPage = response.data.next
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
.cardset-img {
  max-height: 20px;
}
</style>
