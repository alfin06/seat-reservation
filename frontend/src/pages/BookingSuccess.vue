<template>
  <div class="container py-5 text-center">
    <h1 class="text-success">Booking Successful!</h1>
    <p>Your seat has been reserved. You will receive a confirmation email shortly.</p>
    <router-link to="/home" class="btn btn-primary mt-4">Go to Home</router-link>
  </div>
</template>

<script setup>
// No script needed for static success page
</script>

<style scoped>
.text-success {
  color: #28a745;
}
</style>
