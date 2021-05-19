<template>
  <v-container>
    <v-card tile flat outlined>
      <v-card-title class="secondary darken-1 headline" v-if="customCardTitle">
        {{ customCardTitle }}
      </v-card-title>
      <v-card-title class="secondary darken-1 headline" v-else>
        {{ cardsCount }} CARDS
      </v-card-title>
      <v-divider class="mb-5"></v-divider>
      <v-row v-if="initData">
        <v-col
          cols="6"
          md="2"
          v-for="card in cardsData"
          :key="card.id">
          <ul>
            <li class="ns-li mb-2">
              <router-link :to="{ name: 'cardDetail', params: { unique_id: card.unique_id }}">
                <img class="card-img" :src="card.image" :alt="card.name">
              </router-link>
            </li>
            <li class="ns-li">
              <p>
                <router-link :to="{ name: 'cardDetail', params: { unique_id: card.unique_id }}">{{ card.name }}</router-link>
              </p>
            </li>
          </ul>
        </v-col>
      </v-row>
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
  props: ['cards', 'cardSetCode', 'customCardTitle'],
  data () {
    return {
      status: '',
      userQuery: null,
      animated: false,
      errorMsg: null,
      moduleTitle: 'Cards',
      nextPage: null,
      cardsData: [],
      cardsCount: 0,
      cardSetCodeValue: this.cardSetCode,
      path: ''
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  watch: {
    cards: {
      immediate: true,
      deep: true,
      handler (newVal, oldVal) {
        if (newVal) {
          this.cardsData = newVal.results
          this.cardsCount = newVal.count
          this.nextPage = newVal.next
        }
      }
    },
    cardSetCode: function (newVal, oldVal) {
      this.cardSetCodeValue = newVal
    }
  },
  methods: {
    viewMore () {
      var thisVm = this
      axios.get(thisVm.nextPage).then(response => {
        let cards = response.data.results
        for (var i = 0; i < cards.length; i++) {
          thisVm.cardsData.push(cards[i])
        }
        thisVm.nextPage = response.data.next
      })
    },
    initData (apiURL) {
      var thisVm = this
      loadProgressBar()
      axios.get(apiURL).then(response => {
        if (response.data) {
          thisVm.cardsData = response.data.results
          thisVm.status = response.status
          thisVm.cardsCount = response.data.count
          thisVm.nextPage = response.data.next
        }
      })
        .catch(function (error) {
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error(error.response.data)
            console.error(error.response.status)
            console.error(error.response.headers)
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser
            // and an instance of http.ClientRequest in node.js
            console.error(error.request)
          } else {
            // Something happened in setting up the request that triggered an Error
            console.error('Error', error.message)
          }
          console.error(error.config)
        })
    }
  },
  mounted () {
    var thisVm = this
    if (!thisVm.cards) {
      let cardsUrl = this.$constants('cardsUrl')
      if (thisVm.cardSetCodeValue) {
        thisVm.path = `${cardsUrl}?card_set_code=${thisVm.cardSetCodeValue}`
        thisVm.initData(thisVm.path)
      } else {
        thisVm.path = `${cardsUrl}`
        thisVm.initData(thisVm.path)
      }
    }
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
.card-img {
  width: 125px;
}
</style>
