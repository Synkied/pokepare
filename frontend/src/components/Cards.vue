<template>
  <div id="cards" class="container mt-5">
    <h2>{{ moduleTitle }}</h2>
    <h4>{{ dataCounter }} cards</h4>
    <div>
      <template v-if="initData">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-2 col-lg-2 col-md-3 col-sm-4 col-6 mt-3" v-for="card in cardsData" :key="card.id">
              <ul>
                <li class="ns-li mb-2">
                  <a :href="card.url"><img class="card-img" :src="card.image" alt=""></a>
                </li>
                <li class="ns-li">
                  <p ><a :href="card.url">{{ card.name }}</a></p>
                </li>
              </ul>
            </div>
          </div>
          <div v-if="nextPage">
            <button class="btn btn-info mt-5" @click="[viewMore()]">View more</button>
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
  props: ['cards', 'dataCount', 'setCode'],
  data () {
    return {
      status: '',
      userQuery: null,
      animated: false,
      errorMsg: null,
      moduleTitle: 'Cards',
      nextPage: '',
      cardsData: this.cards,
      dataCounter: this.dataCount,
      setCodeValue: this.setCode,
      path: ''
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
          thisVm.dataCounter = response.data.count
          thisVm.nextPage = response.data.next
        }
      })
    }
  },
  components: {
  },
  mounted () {
    var thisVm = this
    if (thisVm.setCodeValue) {
      console.log('pouet')
      thisVm.path = '/api/cards/?card_set_code=' + thisVm.setCodeValue
    } else {
      thisVm.path = '/api/cards/'
    }
    thisVm.initData(thisVm.path)
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
