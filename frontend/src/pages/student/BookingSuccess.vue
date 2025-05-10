<template>
  <el-card class="success-card text-center">
    <div class="checkmark-wrapper">
      <div class="checkmark-circle">
        <div class="checkmark"></div>
      </div>
    </div>
    <h2 class="text-success mt-4">Booking Successful!</h2>
    <p>Your seat has been reserved. You will receive a confirmation email shortly.</p>
    <router-link to="/home">
      <button class="btn btn-outline-primary mt-4">
        <i class="bi bi-arrow-left me-2"></i> Back to Home
      </button>
    </router-link>
  </el-card>
</template>

<script setup>
// No logic needed
</script>

<style scoped>
.success-card {
  max-width: 600px;
  margin: 40px auto;
  padding: 30px;
}

.text-success {
  color: #28a745;
}

/* Animated Checkmark */
.checkmark-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.checkmark-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #e6f4ea;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: scaleIn 0.4s ease;
}

.checkmark {
  width: 40px;
  height: 20px;
  border-left: 5px solid #28a745;
  border-bottom: 5px solid #28a745;
  transform: rotate(-45deg);
  animation: drawCheck 0.4s ease-out 0.2s forwards;
  opacity: 0;
}

@keyframes drawCheck {
  to {
    opacity: 1;
  }
}

@keyframes scaleIn {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>