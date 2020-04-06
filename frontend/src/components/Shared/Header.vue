<!-- Header file, used to define the navbar -->
<!--  Quentin Lathiere - synkx@hotmail.fr -->

<template>
  <div id="header">
    <b-navbar toggleable="md" type="light" variant="faded">

      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="/"><a class="navbar-brand js-scroll-trigger" href="/"><img src="../../assets/pokepare_200.png" height="50" alt="">PokePare</a></b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
          <b-nav-item href="/cards">Cards</b-nav-item>
          <b-nav-item href="/pokemons">Pokémon</b-nav-item>
          <b-nav-item href="/cardsets">Card Sets</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
    <!--     <b-navbar-nav class="ml-auto">

      <b-nav-form>
        <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Pikachu..."/>
        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
      </b-nav-form>

      <b-nav-item-dropdown right>
        Using button-content slot
        <template slot="button-content">
          <em><font-awesome-icon icon="user" size="lg" /></i></em>
        </template>
        <b-dropdown-item href="#">Profile</b-dropdown-item>
        <b-dropdown-item href="#">Signout</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav> -->

      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: 'Header',
  components: {
  }
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Noto+Sans');

  .logo_txt {
    font-family: 'Noto Sans', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: -10px;
    text-align: right;
  }

</style>
