<template>
  <div class="container">
    <div class="col-xl-12 col-12 cell">
      <label class="btn btn-primary">Browse files...
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()" hidden/>
      </label>
      {{ file.name }}
    </div>
    <button class="btn btn-info" v-on:click="submitFile()">Submit</button>
    <div class="mt-4" v-if="errorMsg">
      {{ errorMsg }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

export default {
  /*
    Defines the data used by the component
  */
  data () {
    return {
      file: '',
      card_name: '',
      errorMsg: ''
    }
  },
  methods: {
    /* Submits the file to the server */
    submitFile () {
      var thisVm = this
      /* Initialize the form data */
      let formData = new FormData()

      /* Add the form data we need to submit */
      formData.append('image', this.file)
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
          console.log(response.data)
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
      this.file = this.$refs.file.files[0]
    }
  }
}
</script>

<style>

</style>
