import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  /* what to render depending on the url passed */
  { path: '/', component: 'Home' },
  { path: '/cards/', component: 'Cards' },
  { path: '/cards/:unique_id', component: 'Card' },
  { path: '/pokemons/', component: 'Pokemons' },
  { path: '/pokemons/:name', component: 'Pokemon' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
    /* searches for the component to render depending on the url passed */
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
