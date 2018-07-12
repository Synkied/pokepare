<template>
  <div id="cards" class="container mt-5">
    <h2>{{ module_title }}</h2>
    <h4>{{ data_count }} cards</h4>
    <div>
      <template v-if="!user_query">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-12 mt-3"  v-for="card in cards" :key="card.id">
              <ul>
                <li class="ns-li mb-2">
                  <a :href="card.url"><img class="card-img" :src="card.image" alt=""></a>
                </li>
                <li class="ns-li">
                  <p><a :href="card.url">{{ card.name }}</a></p>
                </li>
              </ul>
            </div>
          </div>
          <div v-if="next_page">
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
  data () {
    return {
      data_count: null,
      page_count: null,
      status: '',
      cards: [],
      user_query: null,
      animated: false,
      error_msg: null,
      module_title: 'Cards',
      next_page: ''
    }
  },
  methods: {
    viewMore () {
      var thisVm = this
      axios.get(thisVm.next_page).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          thisVm.cards.push(response.data.results[i])
        }
        thisVm.next_page = response.data.next
      })
    }
  },
  components: {
  },
  mounted () {
    var thisVm = this
    const path = '/api/cards/'
    loadProgressBar()
    axios.get(path).then(response => {
      if (response.data) {
        console.log(response.status)
        console.log(response.data)
        thisVm.cards = response.data.results
        thisVm.status = response.status
        thisVm.data_count = response.data.count
        thisVm.next_page = response.data.next
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
