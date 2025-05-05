<script>
import { getCSRFToken } from '../../store/auth';
import logo from '@/assets/app_logo.jpg';

export default {
  data() {
    return {
      logo,
      email: '',
      password: '',
      password2: '',
      error: '',
      success: '',
      role: 'STUDENT',
      loading: false,
      roles: [
        { value: 'STUDENT', label: 'Student' },
        { value: 'ADMIN', label: 'Admin' }
      ]
    };
  },
  methods: {
    async register() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      try {
        this.error = '';
        this.loading = true;

        if (!emailRegex.test(this.email)) {
          this.error = 'Invalid email address!';
        } else if (this.password !== this.password2) {
          this.error = 'Passwords do not match!';
        } else {
          const response = await fetch('http://localhost:8000/users/auth/register/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken()
            },
            credentials: 'include',
            body: JSON.stringify({
              email: this.email,
              name: this.email,
              password: this.password,
              confirm_password: this.password2,
              role: this.role
            })
          });

          if (!response.ok) {
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
              const data = await response.json();
              this.error = 'Registration failed: ' + JSON.stringify(data.email);
            } else {
              this.error = 'Registration failed: Please contact the administrator.';
            }
            return;
          }

          this.$notify({
            type: "success",
            text: "Registration successful! Please check your email and verify your account."
          });

          setTimeout(() => this.$router.push('/login'), 1500);
        }
      } catch (err) {
        this.error = 'An error occurred during registration: ' + err;
      } finally {
        this.loading = false;
      }
    },
    onLogin() {
      this.$router.push('/login');
    },
    onForgotPassword() {
      this.$router.push('/forgot-password');
    }
  }
};
</script>

<template>
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <el-card class="box-card" v-loading="loading" element-loading-text="Please wait..." element-loading-spinner="el-icon-loading">
            <div class="text-center mb-4">
              <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 150px;" />
              <h4 class="fw-bold text-primary text-center mb-3">{{ $t('register') }}</h4>
            </div>
  
            <p v-if="error" class="error text-danger text-center">{{ error }}</p>
            <p v-if="success" class="success text-success text-center">{{ success }}</p>
  
            <el-form @submit.prevent="register" class="form-horizontal">
              <el-form-item :label="$t('enterEmail')" class="form-label">
                <el-input v-model="email" type="email" required :placeholder="$t('enterEmail')" />
              </el-form-item>
  
              <el-form-item :label="$t('enterPassword')" class="form-label">
                <el-input v-model="password" type="password" required :placeholder="$t('enterPassword')" />
              </el-form-item>
  
              <el-form-item :label="$t('confirmPassword')" class="form-label">
                <el-input v-model="password2" type="password" required :placeholder="$t('confirmPassword')" />
              </el-form-item>
  
              <!-- Future: Role selection -->
              <!--
              <el-form-item label="Role" class="form-label">
                <el-select v-model="role" placeholder="Select role">
                  <el-option v-for="role in roles" :key="role.value" :label="role.label" :value="role.value" />
                </el-select>
              </el-form-item>
              -->
  
              <el-button type="primary" class="w-100 mt-3" @click="register">{{ $t('submitRegister') }}</el-button>
            </el-form>
  
            <div class="links-container mt-4 text-center">
              <p>
                {{ $t('alreadyHaveAccount') }}?
                <el-link type="primary" @click="onLogin">{{ $t('login') }}</el-link>
              </p>
            </div>
          </el-card>
        </div>
      </div>
    </div>
</template>

<style scoped>
.box-card {
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  background: #fff;
}

.error {
  color: #f56c6c;
  margin-bottom: 1rem;
}

.success {
  color: #67c23a;
  margin-bottom: 1rem;
}

.links-container p {
  margin: 0.5rem 0;
  font-weight: 500;
}

:deep(.el-link) {
  font-weight: 600;
  margin-left: 4px;
}

:deep(.el-form-item) {
  margin-bottom: 1.5rem;
}
</style>