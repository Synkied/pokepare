import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
export default new Vuex.Store(
  {
    state: {
      storedPokemons: [],
      cards: [],
      userLanguage: localStorage.getItem('userLanguage') || 'en'
    },
    getters: {
      getPokemonsFromStore: state => {
        return state.storedPokemons
      },
      getUserLanguage: state => {
        return state.userLanguage
      }
    },
    mutations: {
      setPokemonsToStore (state, pokemons) {
        state.storedPokemons = pokemons
      },
      setUserLanguage (state, language) {
        state.userLanguage = language
      },
      addPokemon (state, pokemon) {
        state.storedPokemons.push(pokemon)
      },
      addcard (state, card) {
        state.cards.push(card)
      }
    }
  }
)
