const CONSTANTS = {
  cardSetsUrl: 'http://localhost:8060/api/cardsets/',
  cardsUrl: 'http://localhost:8060/api/cards/',
  pokemonsUrl: 'http://localhost:8060/api/pokemons/'
}

CONSTANTS.install = function (Vue, options) {
  Vue.prototype.$constants = (key) => {
    return CONSTANTS[key]
  }
}

export default CONSTANTS
