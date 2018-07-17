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
  },
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

table {
  border: 2px solid #42b983;
  border-radius: 3px;
  background-color: #fff;
}

th {
  background-color: #42b983;
  color: rgba(255,255,255,0.66);
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

td {
  background-color: #f9f9f9;
}

th, td {
  min-width: 120px;
  padding: 10px 20px;
}

th.active {
  color: #fff;
}

th.active .arrow {
  opacity: 1;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #fff;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #fff;
}

</style>
