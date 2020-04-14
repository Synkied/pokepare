<template>
  <v-container>
    <div>
      <v-file-input
        show-size
        filled
        dense
        accept="image/*"
        placeholder="Upload a Pokémon card..."
        id="file"
        ref="file"
        v-model="userUploadedFile"
        prepend-icon=""
        prepend-inner-icon="image"
        @change="handleFileUpload()"
      />
    </div>
    <v-btn
      tile
      outlined
      color="primary"
      @click="submitFile()"
    >
      Upload image
    </v-btn>

    <v-snackbar
      :top="true"
      v-model="snackbar.showSnackbar"
      :color="snackbar.color"
      class="color--text"
      :multi-line="snackbar.mode === 'multi-line'"
      :timeout="snackbar.timeout"
      :vertical="snackbar.mode === 'vertical'">
      <span v-if="snackbar.status">
        {{ snackbar.status }}
      </span>
      {{ snackbar.text }}
      <v-btn
        text
        @click="snackbar.showSnackbar = false">
        <v-icon class="color--text">close</v-icon>
      </v-btn>
    </v-snackbar>
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
      userUploadedFile: null,
      snackbar: {
        showSnackbar: false,
        color: '',
        mode: '',
        timeout: 4000,
        text: '',
        errors: ''
      }
    }
  },
  methods: {
    /* Submits the file to the server */
    submitFile () {
      var thisVm = this
      /* Initialize the form data */
      let formData = new FormData()

      if (this.userUploadedFile) {
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
            this.snackbarMessage('No card found for this image.', 'error')
          }
        })
          .catch((err) => {
            console.error(err)
            this.snackbarMessage('A problem occured, please contact the developer.', 'error')
          })
      } else {
        this.snackbarMessage('Please upload an image.', 'warning')
      }
    },
    snackbarMessage (response, color, errors) {
      let okStatus = [200, 201, 202]
      this.snackbar.showSnackbar = false
      this.snackbar.color = color
      this.snackbar.showSnackbar = true
      if (response.status) {
        this.snackbar.status = response.status
        if (okStatus.includes(response.status)) {
          this.snackbar.text = 'File uploaded.'
        } else {
          this.snackbar.text = response.statusText
        }
      } else {
        this.snackbar.text = response
      }
    },
    /* Handles a change on the file upload */
    handleFileUpload () {
    }
  }
}
</script>

<style>

</style>
