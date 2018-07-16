import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  /* what to render depending on the url passed */
  { path: '/', component: 'Home', name: 'home' },
  { path: '/cards/', component: 'Cards', name: 'allCards' },
  { path: '/cards/:unique_id', component: 'Card', name: 'cardDetail' },
  { path: '/pokemons/', component: 'Pokemons', name: 'allPokemons' },
  { path: '/pokemons/:name', component: 'Pokemon', name: 'pokemonDetail' },
  { path: '/sets/', component: 'Sets', name: 'allSets' },
  { path: '/sets/:code', component: 'Set', props: true, name: 'setDetail' },
  { path: '/search/', component: 'Search', props: (route) => ({ query: route.query.query }), name: 'search' }
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
