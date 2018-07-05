<!-- Header file, used to define the navbar -->
<!--  Quentin Lathiere - synkx@hotmail.fr -->

<template>
  <div id="header">
  <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
    <div class="container nav-container">
      <a class="navbar-brand js-scroll-trigger text-light" href=""><img src="../../assets/pokepare_200.png" height="60" alt="">PokePare</a>
      <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link js-scroll-trigger" href="/cards">Cards</a>
          </li>
          <li class="nav-item">
            <a class="nav-link js-scroll-trigger" href="/pokemons">Pokemons</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
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

  .navbar {
    color: #fff;
  }

  nav a, nav a:hover, nav a:active{
    color: #fff;
  }

  .logo_txt {
    font-family: 'Noto Sans', sans-serif;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: -10px;
    text-align: right;
  }

</style>
