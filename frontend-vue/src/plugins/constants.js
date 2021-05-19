const CONSTANTS = {
  cardSetsUrl: '/api/cardsets/',
  cardsUrl: '/api/cards/',
  pokemonsUrl: '/api/pokemons/'
}

CONSTANTS.install = function (Vue, options) {
  Vue.prototype.$constants = (key) => {
    return CONSTANTS[key]
  }
}

export default CONSTANTS
