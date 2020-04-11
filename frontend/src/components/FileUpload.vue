<template>
  <v-container>
    <div>
      <v-file-input
        show-size
        accept="image/*"
        label="Upload a Pokémon card..."
        id="file"
        ref="file"
        v-model="userUploadedFile"
        @change="handleFileUpload()"
      />
    </div>
    <v-btn
      tile
      outlined
      color="primary"
      @click="submitFile()"
    >
      Submit
    </v-btn>
    <div v-if="errorMsg">
      <v-alert class="mt-5" dense outlined type="error">
        {{ errorMsg }}
      </v-alert>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  /*
    Defines the data used by the component
  */
  data () {
    return {
      card_name: '',
      errorMsg: '',
      userUploadedFile: null
    }
  },
  methods: {
    /* Submits the file to the server */
    submitFile () {
      var thisVm = this
      /* Initialize the form data */
      let formData = new FormData()

      /* Add the form data we need to submit */
      formData.append('image', this.userUploadedFile)
      loadProgressBar()
      /* Make the request to the POST /single-file URL */
      axios.post('/file-upload/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(response => {
        if (response.data) {
          thisVm.card_name = response.data.result
        }
        if (thisVm.card_name) {
          window.location.href = '/cards/' + thisVm.card_name
        } else {
          thisVm.errorMsg = 'No card found for this image.'
        }
      })
        .catch(function () {
          console.log('FAILURE!!')
        })
    },
    /* Handles a change on the file upload */
    handleFileUpload () {
    }
  }
}
</script>

<style>

</style>
