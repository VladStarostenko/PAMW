<template>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav class="justify-content-md-center">
        <b-navbar-nav>
          <router-link class="nav-link" to="/">Login</router-link>
          <router-link class="nav-link" to="/register">Register</router-link>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
</template>
