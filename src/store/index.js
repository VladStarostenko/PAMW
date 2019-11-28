import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('usertoken') || '',
    user: {}
  },
  mutations: {
    auth_request (state) {
      state.status = 'loading'
    },
    auth_success (state) {
      state.status = 'success'
    },
    auth_error (state) {
      state.status = 'error'
    }
  },
  actions: {
    async register ({commit}, {firstname, lastname, username, email, password, fileName}) { // Rejestracja
      axios.post('users/register', {
        first_name: firstname,
        last_name: lastname,
        username: username,
        email: email,
        password: password,
        file_name: fileName
      }).then(res => {
        const token = res.data.token
        const user = res.data.user
        localStorage.setItem('usertoken', token)
        axios.defaults.headers.common['Authorization'] = token
        commit('auth_success', token, user)
      }).catch(err => {
        commit('auth_error', err)
      })
    }
  },
  getters: {
    isLoggedIn (state) {
      return state.user !== null
    },
    authStatus: state => state.status
  }
})
