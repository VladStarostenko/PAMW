<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark rounded">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar1" aria-controls="navbar1"
              aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-md-center" id="navbar1">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>

          <li class="nav-item">
            <a href="" class="nav-link" v-on:click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
        <div class="jumbotron mt-5">
            <div class="col-sm-8 mx-auto">
                <h1 class="text-center">PROFILE</h1>
            </div>
            <table class="table col-md-6 mx-auto">
                <tbody>
                    <tr>
                        <td>First Name</td>
                        <td>{{first_name}}</td>
                    </tr>
                    <tr>
                        <td>Last Name</td>
                        <td>{{last_name}}</td>
                    </tr>
                    <tr>
                        <td>Email</td>
                        <td>{{email}}</td>
                    </tr>
                    <tr>
                      <td>Username</td>
                      <td>{{username}}</td>
                    </tr>
                    <tr>
                      <td>File</td>
                      <td>{{filename}}</td>
                    </tr>
                    <v-btn
                      @click="downloadWithAxios"
                      color="blue"
                    >Download document</v-btn>
                    <v-btn
                      @click="deleteFile"
                      color="red"
                    >Delete document</v-btn>
                </tbody>
            </table>
            <v-form v-model="valid" :lazy-validation="lazy" action="" method=post enctype=multipart/form-data id="formElem">
                <v-file-input
                  :rules="[v => !!v || 'Password is required']"
                  v-model="file"
                  placeholder="Upload your documents"
                  label="File input"
                  multiple
                >
                  <template v-slot:selection="{ text }">
                    <v-chip
                      small
                      label
                      color="primary"
                    >
                      {{ text }}
                    </v-chip>
                  </template>
                </v-file-input>
                <v-btn
                  @click="uploadFile"
                  :disabled="!valid"
                  color="success"
                >Add document</v-btn>
            </v-form>
        </div>
    </div>
  </div>
</template>

<script>
import jwtDecode from 'jwt-decode'
import axios from 'axios'

export default {
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      valid: true,
      lazy: false,
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      username: decoded.identity.username,
      filename: decoded.identity.file_name,
      file: null
    }
  },
  mounted: function () {
    console.log(localStorage.getItem('usertoken'))
  },
  methods: {
    logout () {
      localStorage.removeItem('usertoken')
    },
    uploadFile () {
      console.log(this.file[0])
      this.filename = this.file[0].name
      let formData = new FormData()
      formData.append('file', this.file[0])
      axios.post('users/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(res => {
        console.log(res)
        this.updateDate()
      }).catch(err => {
        console.log(err)
      })
    },
    updateDate () {
      axios.post('users/updateDate', {
        file_name: this.filename,
        username: this.username
      }).then(res => {
        console.log(res)
      }).catch(err => {
        console.log(err)
      })
    },
    forceFileDownload (response) {
      console.log(response)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', this.filename)
      // document.body.appendChild(link)
      link.click()
    },
    downloadWithAxios () {
      axios.get('users/download', {params: {file_name: this.filename}, responseType: 'blob'})
        .then(response => {
          this.forceFileDownload(response)
        })
        .catch(() => console.log('error occured'))
    },
    deleteFile () {
      axios.delete('users/deleteFile', {params: {file_name: this.filename, username: this.username}})
        .then(response => {
          this.filename = ''
          console.log(response)
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
