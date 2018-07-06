<template>
  <div id="app">
    <app-header></app-header>
    <!-- Hey! -->
    <router-view/>
    <app-footer></app-footer>
  </div>
</template>

<script>
import Header from './components/Shared/Header.vue'
import Footer from './components/Shared/Footer.vue'

export default {
  name: 'App',
  components: {
    'app-header': Header,
    'app-footer': Footer
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
}

body {
  background-color: rgb(100,185,220)
  /* background-image: radial-gradient(circle,rgba(153,211,223,.95) 10%, rgba(136,187,214,.95) 130%) !important; */
}

</style>
