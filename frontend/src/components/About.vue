<template>
  <v-container>
    <section class="about-us">
      <h1 class="mt-5">What's PokePare?</h1>
      <img class="mb-4" src="../assets/pokepare_200.png" height="40px" alt="">
      <p>PokePare is all about finding the prices for Pokemon cards.</p>
      <p>It's also a bit more, as it has an API built-in to retrieve Pokemons, their cards, and the cards' sets. It is available at: <a href="http://pokepare.com/api/">pokepare.com/api/</a>.</p>
      <p>Some documentation will be written soon.</p>
      <p>The Pokemon' data and cards were built using (a big thank to them!):</p>
      <ul>
        <li class="ns-li"><a href="https://pokeapi.co/">Pokéapi</a></li>
        <li class="ns-li"><a href="http://pokemontcg.io/">PokemonTCG</a></li>
      </ul>
    </section>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      moduleTitle: 'About'
    }
  },
  title () {
    return `PokePare — ${this.moduleTitle}`
  },
  methods: {
  }
}
</script>

<!-- scoped styles for this component -->
<style scoped>
</style>
