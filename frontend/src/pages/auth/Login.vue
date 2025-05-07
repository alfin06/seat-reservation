<script>
import { useAuthStore } from '../../store/auth';
import logo from '@/assets/app_logo.png';

export default {
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      email: "",
      password: "",
      role: "STUDENT",
      error: "",
      logo,
      roles: [
        { label: 'Student', value: 'STUDENT' },
        { label: 'Admin', value: 'ADMIN' }
      ]
    };
  },
  methods: {
    async login() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.error = "Invalid email address!";
        return;
      }

      try {
        await this.authStore.login(
          {
            email: this.email,
            password: this.password
          },
          this.$router
        );
      } catch (error) {
        this.error = "Login failed: Please check your credentials!";
      }
    },
    resetError() {
      this.error = "";
    },
    onRegister() {
      this.$router.push('/register');
    },
    onForgotPassword() {
      this.$router.push('/forgot-password');
    }
  }
};
</script>

<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg p-4 w-100" style="max-width: 480px; border-radius: 1rem;">
      <div class="text-center mb-4">
        <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 150px;" />
      </div>

      <p v-if="error" class="alert alert-danger text-center py-2">{{ error }}</p>

      <el-form @submit.prevent="login" class="mb-3">
        <el-form-item>
          <el-input
            v-model="email"
            type="text"
            placeholder="Email"
            required
            @input="resetError"
            prefix-icon="el-icon-message"
          />
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="password"
            type="password"
            placeholder="Password"
            required
            @input="resetError"
            prefix-icon="el-icon-lock"
          />
        </el-form-item>

        <el-form-item class="d-grid">
          <el-button type="primary" size="large" class="w-100" @click="login">
            {{ $t('submitLogin') }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="text-center">
        <p class="small">
          <el-link type="info" @click="onForgotPassword">{{ $t('forgetPassword') }}?</el-link>
        </p>
        <p class="small">
          {{ $t('noAccount') }}?
          <el-link type="primary" @click="onRegister">{{ $t('register') }}</el-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  background-color: #fff;
  border: none;
}

.el-input {
  --el-input-border-radius: 0.5rem;
}

.el-button {
  border-radius: 0.5rem;
}

.el-form-item {
  margin-bottom: 1rem;
}
</style>
