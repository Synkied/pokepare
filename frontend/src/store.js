import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
export default new Vuex.Store(
  {
    state: {
      storedPokemons: [],
      pokemonsPage: 1,
      pokemonsByPage: 60,
      cards: [],
      userLanguage: localStorage.getItem('userLanguage') || 'en'
    },
    getters: {
      getPokemonsFromStore: state => {
        return state.storedPokemons
      },
      getUserLanguage: state => {
        return state.userLanguage
      },
      getPokemonsPage: state => {
        return state.pokemonsPage
      },
      getPokemonsByPage: state => {
        return state.pokemonsByPage
      }
    },
    mutations: {
      setPokemonsToStore (state, pokemons) {
        state.storedPokemons = pokemons
      },
      setPokemonsPage (state, page) {
        state.pokemonsPage = page
      },
      setPokemonsByPage (state, byPage) {
        state.pokemonsByPage = byPage
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
