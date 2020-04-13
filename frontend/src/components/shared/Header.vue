<!-- Header file, used to define the navbar -->
<!--  Quentin Lathiere - synkx@hotmail.fr -->

<template>
  <div>
    <v-app-bar
      dark
      flat
      app
    >
      <a class="d-flex align-center white--text" href="/">
        <img src="../../assets/pokepare_200.png" height="50" alt=""/>
        <span class="headline ml-1">POKEPARE</span>
      </a>
      <v-spacer></v-spacer>
      <v-container id="app-bar-search-bar">
        <search-bar></search-bar>
      </v-container>
      <v-btn text small to="/cards">Cards</v-btn>
      <v-btn text small to="/pokemons">Pokemon</v-btn>
      <v-btn text small to="/cardsets">Cards Sets</v-btn>
      <v-btn icon small to="#">
        <v-icon>
          face
        </v-icon>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import SearchBar from '../SearchBar'

export default {
  name: 'Header',
  components: {
    'search-bar': SearchBar
  },
  data () {
    return {}
  }
}
</script>

<style>
.container#app-bar-search-bar {
  max-width: 500px;
}

</style>
