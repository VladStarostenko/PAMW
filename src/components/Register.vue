<template>
  <div>
    <navbar></navbar>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
              <v-form
                ref="form"
                v-model="valid"
                :lazy-validation="lazy"
              >
                <h1 class="h3 mb-3 font-weight-normal">Please sign up</h1>
                <v-text-field
                  v-model="first_name"
                  :counter="10"
                  :rules="firstNameRules"
                  label="First Name"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="last_name"
                  :counter="15"
                  :rules="lastNameRules"
                  label="Last Name"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="email"
                  :rules="emailRules"
                  label="E-mail"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="username"
                  @blur = "this.checkUser"
                  :rules="[this.statUs || 'Login already exists', v => !!v || 'Login name is required', v => (v && v.length <= 10) || 'First name must be less than 10 characters', v => /^[A-z]/.test(v) || 'First name must consist of letters']"
                  label="Login"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  :rules="passwordRules"
                  label="Password"
                  type="password"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="confirmPassword"
                  :rules="[v => v === this.password|| 'Password should match', v => !!v || 'Password is required']"
                  label="Confirm Password"
                  type="password"
                  required
                ></v-text-field>
                <v-btn
                  color="error"
                  class="mr-4"
                  @click="reset"
                >
                  Reset Form
                </v-btn>

                <v-btn
                  class="mr-4"
                  @click="register"
                  :disabled="!valid"
                  color="success"
                >
                  Submit
                </v-btn>
              </v-form>
            </div>
        </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import router from '../router'
import Navbar from '../components/Navbar'

export default {
  data () {
    return {
      file_name: '',
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      valid: true,
      lazy: false,
      statUs: false,
      firstNameRules: [
        v => !!v || 'First name is required',
        v => (v && v.length <= 10) || 'First name must be less than 10 characters',
        v => /^[A-z]/.test(v) || 'First name must consist of letters'
      ],
      lastNameRules: [
        v => !!v || 'Last name is required',
        v => (v && v.length <= 15) || 'Last name must be less than 15 characters',
        v => /^[A-z]/.test(v) || 'Last name must consist of letters'
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ],
      usernameRules: [
        v => !!v || 'Login name is required',
        v => (v && v.length <= 10) || 'First name must be less than 10 characters',
        v => /^[A-z]/.test(v) || 'First name must consist of letters'
      ],
      passwordRules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 6) || 'Password must be bigger  than 6 characters'
      ]
    }
  },
  beforeUpdate: async function checkUser () {
    const result = axios.get('users/checkUser', {params: {username: this.username}})
    var result1 = await result
    if (result1.data === 'Free') {
      this.statUs = true
    } else {
      this.statUs = false
    }
  },
  components: {
    'Navbar': Navbar
  },
  methods: {
    reset () {
      this.$refs.form.reset()
    },
    checkUser () {
      axios.get('users/checkUser', {params: {username: this.username}})
        .then(res => {
          if (res.data === 'Free') {
            this.statUs = true
          } else {
            this.statUs = false
          }
        })
    },
    async register () {
      const user = {
        firstname: this.first_name,
        lastname: this.last_name,
        username: this.username,
        email: this.email,
        password: this.password,
        fileName: this.file_name
      }
      this.$store.dispatch('register', user)
        .then(res => {
          router.push({name: '/'})
        }).catch(err => {
          console.log(err)
        })
    }
  }
}

</script>

<style>
  h3{
    text-align: center;
    padding: 15px;
    font-size: xx-large;
    color: #d2be14
  }
  p{
    text-align: center;
    font-size: large;
    color: #211610;
  }
  form{
    padding: 2em;
    border-radius: 10px;
    border-color: #1a210c;
    border-style: solid;
  }
  form h1 {
    margin: 0;
    position: absolute;
    left: 50%;
    margin-right: -50%;
    transform: translate(-50%, -50%) }
</style>
