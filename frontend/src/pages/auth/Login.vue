<script>
import { useAuthStore } from '../../store/auth';
import logo from '@/assets/app_logo.png';
import { notify } from "@kyvg/vue3-notification";

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
        notify({ type: "error", title: 'ERROR', duration: 3000, text: "Invalid email address!" });
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
        notify({ type: "error", title: 'LOGIN FAILED', duration: 3000, text: "Please check your credentials!" });
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
  <div class="container d-flex justify-content-center align-items-center login">
    <div class="card shadow p-4 w-100" style="max-width: 400px; border-radius: 1rem;">
      <div class="text-center mb-3">
        <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 180px;" />
      </div>
      <br/>
      <p v-if="error" class="alert alert-danger text-center py-2 mb-2">{{ error }}</p>

      <el-form @submit.prevent="login" class="mb-2">
        <el-form-item class="mb-3">
          <el-input
            v-model="email"
            type="text"
            placeholder="Email"
            required
            @input="resetError"
            prefix-icon="el-icon-message"
          />
        </el-form-item>

        <el-form-item class="mb-3">
          <el-input
            v-model="password"
            type="password"
            placeholder="Password"
            required
            show-password
            clearable
            @input="resetError"
            prefix-icon="el-icon-lock"
          />
        </el-form-item>
        <br/>

        <el-form-item class="mb-2">
          <el-button type="primary" size="large" class="w-100" @click="login">
            {{ $t('submitLogin') }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="text-center small bottom">
        <el-link type="primary" @click="onForgotPassword">{{ $t('forgetPassword') }}?</el-link><br />
        {{ $t('noAccount') }}?
        <el-link type="primary" @click="onRegister">{{ $t('register') }}</el-link>
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

.login {
  margin-top:10%;
  font-size: 14pt;
  padding: 15px;
}

.bottom {
  margin-top: 15px;
  padding-top:5px;
  padding-bottom: 5px;
}
</style>