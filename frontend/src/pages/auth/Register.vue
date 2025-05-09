<script>
import { getCSRFToken } from '../../store/auth';
import logo from '@/assets/app_logo.png';

export default {
  data() {
    return {
      logo,
      name: '',
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
          notify({ type: "error", title: 'ERROR', duration: 3000, text: "Invalid email address!" });
        } else if (this.password !== this.password2) {
          notify({ type: "error", title: 'ERROR', duration: 3000, text: "Passwords do not match!" });
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
              name: this.name,
              password: this.password,
              confirm_password: this.password2,
              role: this.role
            })
          });

          if (!response.ok) {
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
              const data = await response.json();
              this.$notify({
                title: "ERROR",
                type: "error",
                duration: 3000,
                text: 'Registration failed: ' + data.email
              });
            } else {
              this.$notify({
                title: "ERROR",
                type: "error",
                duration: 3000,
                text: "Registration failed: Please contact the administrator."
              });
            }
            return;
          }

          this.$notify({
            title: "SUCCESS",
            type: "success",
            duration: 3000,
            text: "Registration successful! Please check your inbox/spam and verify your account."
          });

          setTimeout(() => this.$router.push('/login'), 1500);
        }
      } catch (err) {
        this.$notify({
            title: "ERROR",
            type: "error",
            duration: 3000,
            text: "An error occurred during registration. Please reload the page and try to register again. If the error is still persisting, please contact the admin."
        });
        console.log('An error occurred during registration: ' + err);
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
    <div class="container justify-content-center align-items-center register">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="box-card" v-loading="loading" element-loading-text="Please wait..." element-loading-spinner="el-icon-loading">
            <div class="text-center mb-4">
              <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 150px;" />
            </div>
  
            <p v-if="error" class="error text-danger text-center">{{ error }}</p>
            <p v-if="success" class="success text-success text-center">{{ success }}</p>
  
            <el-form @submit.prevent="register" label-position="top" class="p-3">
              <el-form-item :label="$t('enterName')">
                <el-input
                  v-model="name"
                  type="text"
                  required
                  :placeholder="$t('enterName')"
                  clearable
                  class="underline-input"/>
              </el-form-item>

              <el-form-item :label="$t('enterEmail')">
                <el-input
                  v-model="email"
                  type="email"
                  required
                  :placeholder="$t('enterEmail')"
                  clearable
                  class="underline-input"/>
              </el-form-item>

              <el-form-item :label="$t('enterPassword')">
                <el-input
                  v-model="password"
                  type="password"
                  required
                  :placeholder="$t('enterPassword')"
                  show-password
                  clearable
                  class="underline-input" />
              </el-form-item>

              <el-form-item :label="$t('confirmPassword')">
                <el-input
                  v-model="password2"
                  type="password"
                  required
                  :placeholder="$t('confirmPassword')"
                  show-password
                  clearable
                  class="underline-input" />
              </el-form-item>

              <el-form-item class="mb-0">
                <el-button type="primary" class="w-100" @click="register">
                  {{ $t('submitRegister') }}
                </el-button>
              </el-form-item>
            </el-form>

            <div class="links-container mt-4 text-center">
              <p>
                {{ $t('alreadyHaveAccount') }}?
                <el-link type="primary" @click="onLogin">{{ $t('login') }}</el-link>
              </p>
            </div>
          </div>
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

.register {
  margin-top:5%;
  padding: 15px;
}

:deep(.el-form-item__label) {
  font-weight: bold;
}

.underline-input .el-input__inner {
  border: none;
  border-bottom: 2px solid #ccc;
  border-radius: 0;
  box-shadow: none;
  padding-left: 0;
  padding-right: 0;
}

.underline-input .el-input__inner:focus {
  border-bottom-color: #409eff; /* Element Plus primary color */
}
</style>