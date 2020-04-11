<!-- Footer file -->
<!--  Quentin Lathiere - synkx@hotmail.fr -->

<template>
  <v-footer
    dark
    absolute
    padless
  >
    <v-card
      class="flex"
      flat
      tile
    >
      <v-card-text class="py-0 primary text-center">
        <v-btn
          v-for="link in links"
          :key="link.id"
          color="white"
          text
          rounded
          class="my-2"
          :href="link.link_to"
        >
          <span v-if="link.icon">
            <v-icon>{{ link.icon }}</v-icon>
          </span>
          <span v-else>
            {{ link.label }}
          </span>
        </v-btn>
      </v-card-text>
      <v-card-text class="py-2 white--text text-center">
        This website is not produced, endorsed, supported, or affiliated with Nintendo or The Pokémon Company — {{ new Date().getFullYear() }}
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {
  data () {
    return {
      links: [
        { label: 'About', link_to: '/about', icon: '' },
        { label: 'Github', link_to: 'https://github.com/Synkied/pokepare', icon: 'fab fa-github' }
      ]
    }
  }
}
</script>

<style>
  footer {
    width: 100%;
    margin: auto;
    margin-top: 100px;
    padding: 15px;
    color: #000;
    text-align: right;
    font-size: 16px;
  }

  footer a {
    color: #000;
    text-decoration: none;
  }

  footer a:hover {
    color: #17252A;
    text-decoration: none;
  }

</style>
