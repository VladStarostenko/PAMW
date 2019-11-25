<template>
  <div>
    <navbar></navbar>
    <div class="container">
      <div class="jumbotron mt-5">
        <div class="col-sm-8 mx-auto">
          <h1 class="text-center">WELCOME</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar'

export default {
  components: {
    'Navbar': Navbar
  }
}
</script>
