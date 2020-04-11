<template>
  <v-app>
    <app-header></app-header>
    <v-content>
      <v-container class="body-container">
        <router-view/>
      </v-container>
      <app-footer></app-footer>
    </v-content>
  </v-app>
</template>

<script>
import Header from './components/shared/Header.vue'
import Footer from './components/shared/Footer.vue'
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
@import url('https://fonts.googleapis.com/css?family=Avenir');
@import url('https://fonts.googleapis.com/css?family=Oswald');
@import url('https://fonts.googleapis.com/css?family=Cabin');
@import url('https://fonts.googleapis.com/css?family=Raleway');
@import url('https://fonts.googleapis.com/css?family=Oxygen');
@import url('https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900');
@import url('https://fonts.googleapis.com/css?family=Material+Icons');
@import url('https://use.fontawesome.com/releases/v5.0.13/css/all.css');

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
/*  background-color: #EEE;
*/}

.body-container {
  padding-bottom: 100px;
}

.container {
  max-width: 1500px;
}

.v-application a {
  text-decoration: none;
  color: #fff
}

a:hover {
  text-decoration: none;
}

.card-title{
  font-family: 'Oswald', sans-serif;
  font-weight: 600;
}

.card-title a{
  color: #0db4b9;
}

.card-title a:hover {
  text-decoration: none;
}

.related-pokemon-image {
  width: 100px;
  margin: auto;
}

.pokemon-link p {
  margin: -10px 0 30px 0;
}

h1{
  text-align: center;
  font-family: 'Cabin', sans-serif;
  font-weight: bold;
  font-size: 2.5rem;
  text-transform: uppercase;
  color: #000;
}

h2 {
  font-family: 'Cabin', sans-serif;
  font-size: 2rem;
  font-weight: 700;
}

h3 small {
  font-size: 60%;
  color: #6f6f6f;
  line-height: 0;
}

.ns-li {
  list-style-type: none;
  font-weight: 600;
}

.ns-li a {
  text-decoration: none;
}

.ns-li a:hover {
  text-decoration: none;
}

.ns-li p {
  font-size: 1rem;
  text-align:center;
}

ul {
  padding: 0;
}

/*table {
  border: 2px solid #42b983;
  border-radius: 3px;
  background-color: #000;
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
  color: #000;
}

th.active .arrow {
  opacity: 1;
}
*/
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
  border-bottom: 4px solid #000;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #000;
}

</style>
