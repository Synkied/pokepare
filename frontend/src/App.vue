<template>
  <div id="app">
    <app-header></app-header>
    <!-- Hey! -->
    <search-bar></search-bar>
    <router-view/>
    <app-footer></app-footer>
  </div>
</template>

<script>
import Header from './components/Shared/Header.vue'
import Footer from './components/Shared/Footer.vue'
import SearchBar from './components/SearchBar.vue'

export default {
  name: 'App',
  components: {
    'app-header': Header,
    'app-footer': Footer,
    'search-bar': SearchBar
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  background-color: rgb(100,185,220);
}

body {
  /* background-image: radial-gradient(circle,rgba(153,211,223,.95) 10%, rgba(136,187,214,.95) 130%) !important; */
}

h1{
  text-align: center;
  font-family: 'Oxygen', sans-serif;
  font-weight: bold;
  font-size: 2.5rem;
  text-transform: uppercase;
  color: #fff;
}

h2 {
  font-family: 'Oxygen', sans-serif;
  font-size: 2rem;
  font-weight: 700;
}

.ns-li {
  list-style-type: none;
  font-family: "Oxygen", sans-serif;
  font-weight: 700;
}

.ns-li a {
  color: #fff;
  text-decoration: none;
}

.ns-li a:hover {
  color: #0e5c59;
  text-decoration: none;
}

.ns-li p {
  font-size: 1rem;
  text-align:center;
}

ul {
  padding: 0;
}

</style>
