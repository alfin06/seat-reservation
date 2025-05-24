<template>
  <div class="forgot-wrapper">
    <div class="box-card">
      <div class="logo-container">
        <img :src="logo" alt="App Logo" class="logo" />
      </div>
      <h2 class="title">Reset Password</h2>
      <p class="description">
        Enter the email address you used during registration. We'll send you instructions to reset your password.
      </p>

      <el-form @submit.prevent="resetPassword" class="form">
        <el-input
          v-model="email"
          type="email"
          placeholder="Enter email"
        />
        <el-button
          type="primary"
          class="submit-btn"
          @click="resetPassword"
          :loading="loading"
        >
          Send Instructions
        </el-button>
      </el-form>

      <div class="links-container">
        <p>
          Remember your password?
          <el-link type="primary" @click="onLogin">Login</el-link>
        </p>
      </div>
    </div>

    <div class="lang-switcher">
      <a
        href="#"
        :class="{ active: currentLanguage === 'en' }"
        @click.prevent="changeLanguage('en')"
      >English</a>
      <span>|</span>
      <a
        href="#"
        :class="{ active: currentLanguage === 'zh' }"
        @click.prevent="changeLanguage('zh')"
      >中文</a>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/store/auth'
import logo from '@/assets/app_logo.png'
import { ElNotification } from 'element-plus'

const email = ref('')
const loading = ref(false)
const { locale } = useI18n()
const currentLanguage = ref(locale.value)

const changeLanguage = (lang) => {
  locale.value = lang
  currentLanguage.value = lang
}

const resetPassword = async () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    ElNotification.error({ title: 'Error', message: 'Invalid email address!' })
    return
  }

  try {
    loading.value = true
    const authStore = useAuthStore()
    await authStore.resetPassword(email.value)
    ElNotification.success({
      title: 'Success',
      message: 'Password reset instructions have been sent to your email.'
    })
  } catch (error) {
    ElNotification.error({
      title: 'Error',
      message: error.message || 'Failed to send reset instructions.'
    })
  } finally {
    loading.value = false
  }
}

const onLogin = () => {
  window.location.href = '/login'
}
</script>

<style scoped>
.forgot-wrapper {
  min-height: 100vh;
  background: #f7f9fc;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.box-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 40px;
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.logo-container {
  margin-bottom: 24px;
}

.logo {
  max-height: 90px;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 12px;
  color: #303133;
}

.description {
  color: #606266;
  margin-bottom: 24px;
  font-size: 0.95rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.submit-btn {
  width: 100%;
  height: 44px;
  font-weight: 600;
}

.links-container {
  margin-top: 24px;
  font-size: 0.95rem;
  color: #606266;
}

.links-container a {
  margin-left: 4px;
}

/* Language Switcher – matches login page style */
.lang-switcher {
  margin-top: 40px;
  font-size: 14px;
  color: #606266;
}

.lang-switcher a {
  color: #606266;
  text-decoration: none;
  margin: 0 6px;
  font-weight: 500;
}

.lang-switcher a.active {
  font-weight: 600;
  color: #409eff;
}
</style>
