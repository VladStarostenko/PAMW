<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav class="justify-content-md-center">
        <b-navbar-nav>
          <router-link class="nav-link" to="/profile">Profile</router-link>
          <a href="/" class="nav-link" v-on:click="logout">Logout</a>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
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
                </tbody>
            </table>
            <div class="col-sm-8 mx-auto">
              <h1 class="text-center">MY FILE</h1>
            </div>
          <table v-for="(filein, i) in filename" :key="i" class="table col-md-6 mx-auto">
            <template>
              <tbody>
                <tr>
                  <td>My file</td>
                  <td>{{filein}}</td>
                  <v-btn
                    @click="downloadWithAxios(filename[i])"
                    color="success"
                  >Download</v-btn>
                  <v-btn
                    @click="deleteFile(filein)"
                    icon
                    style="margin-left: 2em"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </tr>
              </tbody>
            </template>
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
                  @click="uploadFiles"
                  :disabled="!valid"
                  color="blue-grey"
                  class="ma-2 white--text"
                >
                  Upload
                  <v-icon right dark>mdi-cloud-upload</v-icon>
                </v-btn>
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
    this.getFileNames()
  },
  methods: {
    logout () {
      localStorage.removeItem('usertoken')
    },
    getFileNames () {
      axios.get('https://vuejs-flask-api.herokuapp.com/users/getFileNames', {params: {username: this.username}})
        .then(res => {
          this.filename = res.data.file_name
        })
        .catch(err =>
          console.log(err))
    },
    uploadFiles () {
      for (let i = 0; i < this.file.length; i++) {
        this.uploadFile(this.file[i])
      }
    },
    uploadFile (file) {
      let formData = new FormData()
      formData.append('file', file)
      formData.append('username', this.username)
      axios.post('https://vuejs-flask-api.herokuapp.com/users/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(res => {
        this.updateDate(file)
      }).catch(err => {
        console.log(err)
      })
    },
    updateDate (file) {
      axios.post('https://vuejs-flask-api.herokuapp.com/users/updateDate', {
        file_name: file.name,
        username: this.username
      }).then(res => {
        this.filename = res.data.file_name
      }).catch(err => {
        console.log(err)
      })
    },
    forceFileDownload (response) {
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', response.config.params.file_name)
      link.click()
    },
    downloadWithAxios (filein) {
      axios.get('https://vuejs-flask-api.herokuapp.com/users/download', {params: {file_name: filein, username: this.username}, responseType: 'blob'})
        .then(response => {
          this.forceFileDownload(response)
        })
        .catch(() => console.log('error occured'))
    },
    deleteFile (filein) {
      axios.delete('https://vuejs-flask-api.herokuapp.com/users/deleteFile', {params: {username: this.username, file_name: filein}})
        .then(res => {
          this.filename = res.data.file_name
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
