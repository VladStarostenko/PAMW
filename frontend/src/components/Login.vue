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
                <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>

                <v-text-field
                  v-model="username"
                  :rules="usernameRules"
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

                <v-btn
                  color="error"
                  class="mr-4"
                  @click="reset"
                >
                  Reset Form
                </v-btn>

                <v-btn
                  class="mr-4"
                  @click="login"
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
import Navbar from '../components/Navbar'

export default {
  data () {
    return {
      username: '',
      password: '',
      valid: true,
      lazy: false,
      usernameRules: [
        v => !!v || 'Login name is required'
      ],
      passwordRules: [
        v => !!v || 'Password is required'
      ]
    }
  },
  components: {
    'Navbar': Navbar
  },
  mounted: function () {
    localStorage.removeItem('usertoken')
  },
  methods: {
    reset () {
      this.$refs.form.reset()
    },
    login () {
      axios.post('https://vuejs-flask-api.herokuapp.com/users/login', {
        username: this.username,
        password: this.password
      }).then(res => {
        if (res.data.token !== undefined) {
          localStorage.setItem('usertoken', res.data.token)
          this.$store.commit('auth_success')
          this.$router.push('/profile').catch(err => { console.log(err) })
        } else {
          alert('Invalid username and password')
          this.reset()
        }
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>
