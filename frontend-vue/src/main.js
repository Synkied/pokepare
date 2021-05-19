// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import store from './store'
import titleMixin from './mixins/titleMixin'
import constants from './plugins/constants.js'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import clipboard from 'v-clipboard'

Vue.mixin(titleMixin)

Vue.config.productionTip = false
Vue.use(constants)
Vue.use(clipboard)

require('vue2-animate/dist/vue2-animate.min.css')

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  vuetify,
  components: {
    App
  },
  template: '<App/>'
})
