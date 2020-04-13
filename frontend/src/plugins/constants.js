const CONSTANTS = {
  cardSetsURL: 'http://localhost:8060/api/cardsets/',
  cardsURL: 'http://localhost:8060/api/cards/',
  pokemonURL: 'http://localhost:8060/api/pokemons/'
}

CONSTANTS.install = function (Vue, options) {
  Vue.prototype.$constants = (key) => {
    return CONSTANTS[key]
  }
}

export default CONSTANTS
