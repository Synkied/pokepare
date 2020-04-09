const CONSTANTS = {
  cardSetsURL: '/api/cardsets/',
  cardsURL: '/api/cards/',
  pokemonURL: '/api/pokemons/'
}

CONSTANTS.install = function (Vue, options) {
  Vue.prototype.$constants = (key) => {
    return CONSTANTS[key]
  }
}

export default CONSTANTS
