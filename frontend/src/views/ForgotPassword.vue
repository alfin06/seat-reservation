<template>
  <div class="auth-form">
    <h2>Reset Password</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <input v-model="email" type="email" placeholder="your@email.com" required>
      </div>
      <button type="submit" class="auth-button">Send Reset Link</button>
    </form>
    <p class="auth-link">
      Remember your password? <router-link to="/login">Login here</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: ''
    }
  },
  methods: {
    handleSubmit() {
      // Add your password reset logic here
      console.log('Reset requested for:', this.email)
    }
  }
}
</script>

<style scoped>
/* Copied exactly from Login.vue to maintain identical styling */
.auth-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.auth-button {
  width: 100%;
  padding: 12px;
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.auth-button:hover {
  background-color: #535bf2;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  color: #7f8c8d;
}

.auth-link a {
  color: #646cff;
  text-decoration: none;
  font-weight: 500;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>