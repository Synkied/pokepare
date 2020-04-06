import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  /* what to render depending on the url passed */
  { path: '/', component: 'Home', name: 'home' },
  { path: '/cards/', component: 'Cards', name: 'allCards' },
  { path: '/cards/:unique_id', component: 'Card', name: 'cardDetail' },
  { path: '/pokemons/', component: 'Pokemons', name: 'allPokemons' },
  { path: '/pokemons/:name', component: 'Pokemon', name: 'pokemonDetail' },
  { path: '/cardsets/', component: 'CardSets', name: 'allCardSets' },
  { path: '/cardsets/:code', component: 'CardSet', props: true, name: 'cardSetDetail' },
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
