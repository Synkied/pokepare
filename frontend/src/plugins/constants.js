const CONSTANTS = {
  cardSetsUrl: '/api/cardset/',
  cardsUrl: '/api/card/',
  pokemonsUrl: '/api/pokemon/',
  languagesUrl: '/api/language/'
}

CONSTANTS.install = function (Vue, options) {
  Vue.prototype.$constants = (key) => {
    return CONSTANTS[key]
  }
}

export default CONSTANTS
