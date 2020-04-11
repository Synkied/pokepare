import 'material-design-icons-iconfont/dist/material-design-icons.css'
import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
// import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import themes from './themes'

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(Vuetify)

const opts = {
  icons: {
    iconfont: 'md'
  },
  theme: {
    dark: true,
    themes: themes
  }
}

export default new Vuetify(opts)
