<template>
  <div id="sets" class="container mt-5">
    <h2>{{ moduleTitle }}</h2>
    <h4>{{ dataCount }} sets</h4>
    <div>
      <template v-if="!userQuery">
        <div class="container-fluid">
          <div class="row">
            <div class="col-xl-4 col-lg-4 col-md-3 col-sm-4 col-6 mt-5"  v-for="set in sets" :key="set.id">
              <ul>
                <li class="ns-li mb-2">
                  <a :href="set.url"><img class="set-img" :src="set.image" height="35px" alt=""></a>
                </li>
                <li class="ns-li">
                  <p><a :href="set.url">{{ set.name }}</a></p>
                </li>
              </ul>
            </div>
          </div>
          <div v-if="next">
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
  props: ['setCodes'],
  data () {
    return {
      dataCount: null,
      pageCount: null,
      status: '',
      sets: [],
      userQuery: null,
      animated: false,
      errorMsg: null,
      moduleTitle: 'Sets',
      next: '',
      setCodesValues: this.setCodes
    }
  },
  methods: {
    viewMore () {
      var thisVm = this
      axios.get(thisVm.next).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          thisVm.sets.push(response.data.results[i])
        }
        thisVm.next = response.data.next
      })
    },
    viewSets () {
      var thisVm = this
      const path = '/api/sets/'
      loadProgressBar()
      axios.get(path).then(response => {
        if (response.data) {
          console.log(response.status)
          console.log(response.data)
          thisVm.sets = response.data.results
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
  @import url('https://fonts.googleapis.com/css?family=Oxygen');
  @import url('https://fonts.googleapis.com/css?family=Raleway');

  .container {
    max-width: 960px;
  }

</style>
