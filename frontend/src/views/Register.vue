<template>
  <div class="auth-form">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>Full Name</label>
        <input 
          v-model="form.name" 
          type="text" 
          placeholder="John Doe" 
          required
        >
      </div>

      <div class="form-group">
        <label>Email</label>
        <input 
          v-model="form.email" 
          type="email" 
          placeholder="your@email.com" 
          required
        >
      </div>

      <div class="form-group">
        <label>Password</label>
        <input 
          v-model="form.password" 
          type="password" 
          placeholder="••••••••" 
          required
        >
        <small class="hint">At least 8 characters</small>
      </div>

      <div class="form-group">
        <label>Confirm Password</label>
        <input 
          v-model="form.confirm_password" 
          type="password" 
          placeholder="••••••••" 
          required
        >
      </div>

      <div class="form-group">
        <label>Role</label>
        <div class="role-options">
          <label>
            <input 
              type="radio" 
              v-model="form.role" 
              value="STUDENT" 
              checked
            >
            <span class="radio-label">Student</span>
          </label>
          <label>
            <input 
              type="radio" 
              v-model="form.role" 
              value="ADMIN"
            >
            <span class="radio-label">Admin</span>
          </label>
        </div>
      </div>

      <button type="submit" class="auth-button">
        Register
      </button>
    </form>

    <p class="auth-link">
      Already have an account? 
      <router-link to="/login">Login here</router-link>
      <!-- NEW: Forgot Password Link -->
      <span style="margin: 0 5px">•</span>
      <router-link to="/forgot-password">Forgot password?</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        confirm_password: '',
        role: 'STUDENT'
      }
    }
  },
  methods: {
    handleRegister() {
      if (this.form.password !== this.form.confirm_password) {
        alert("Passwords don't match!");
        return;
      }
      // Your existing registration logic
    }
  }
}
</script>

<style scoped>
/* All existing styles remain unchanged */
.auth-form {
  max-width: 500px;
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

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.hint {
  display: block;
  margin-top: 5px;
  color: #7f8c8d;
  font-size: 0.85rem;
}

.role-options {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.role-options label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
}

.radio-label {
  position: relative;
  top: -1px;
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
  margin-top: 10px;
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