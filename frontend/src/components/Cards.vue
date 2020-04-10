<template>
  <div id="cards" class="container mt-5">
    <h4>{{ cardsCount }} cards found</h4>
    <div>
      <template v-if="initData">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-2 col-lg-2 col-md-3 col-sm-4 col-6 mt-3" v-for="card in cardsData" :key="card.id">
              <ul>
                <li class="ns-li mb-2">
                  <a :href="card.url"><img class="card-img" :src="card.image" :alt="card.name"></a>
                </li>
                <li class="ns-li">
                  <p><a :href="card.url">{{ card.name }}</a></p>
                </li>
              </ul>
            </div>
          </div>
          <div v-if="nextPage">
            <button class="btn btn-info mt-5" @click="viewMore()">View more</button>
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
  props: ['cards', 'cardSetCode'],
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
    cards: function (newVal, oldVal) {
      this.cardsData = this.cards.results
      this.cardsCount = this.cards.count
      this.nextPage = this.cards.next
    },
    cardSetCode: function (newVal, oldVal) {
      this.cardSetCodeValue = newVal
    }
  },
  methods: {
    viewMore () {
      var thisVm = this
      axios.get(thisVm.nextPage).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          thisVm.cardsData.push(response.data.results[i])
        }
        thisVm.nextPage = response.data.next
      })
    },
    initData (path) {
      var thisVm = this
      loadProgressBar()
      axios.get(path).then(response => {
        if (response.data) {
          console.log('cards status:', response.status)
          console.log(response.data)
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
  },
  mounted () {
    var thisVm = this
    if (!thisVm.cards) {
      let cardsURL = this.$constants('cardsURL')
      if (thisVm.cardSetCodeValue) {
        thisVm.path = `${cardsURL}?card_set_code=${thisVm.cardSetCodeValue}`
        thisVm.initData(thisVm.path)
      } else {
        thisVm.path = `${cardsURL}`
        thisVm.initData(thisVm.path)
      }
    }
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>

  .container {
    max-width: 960px;
  }

</style>
