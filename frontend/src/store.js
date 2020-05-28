import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
export default new Vuex.Store(
  {
    state: {
      pokemons: [],
      cards: []
    },
    getters: {
    },
    mutations: {
      addPokemon (state, pokemon) {
        state.pokemons.push(pokemon)
      },
      addcard (state, card) {
        state.cards.push(card)
      }
    }
  }
)
