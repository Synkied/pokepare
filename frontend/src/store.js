import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
export default new Vuex.Store(
  {
    state: {
      pokemons: [],
      cards: [],
      userLanguage: 'en'
    },
    getters: {
      getUserLanguage: state => {
        return state.userLanguage
      }
    },
    mutations: {
      addPokemon (state, pokemon) {
        state.pokemons.push(pokemon)
      },
      addcard (state, card) {
        state.cards.push(card)
      },
      setUserLanguage (state, languageSelected) {
        state.userLanguage = languageSelected
      }
    }
  }
)
