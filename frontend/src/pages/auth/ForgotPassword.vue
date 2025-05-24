<template>
  <div class="forgot-wrapper">
    <div class="box-card">
      <div class="logo-container">
        <img :src="logo" alt="App Logo" class="logo" />
      </div>
      <h2 class="title">{{ $t('resetPasswordTitle') }}</h2>
      <p class="description">{{ $t('forgotInstruction') }}</p>

      <el-form @submit.prevent="resetPassword" class="form">
        <el-input
          v-model="email"
          type="email"
          :placeholder="$t('enterEmail')"
        />
        <el-button
          type="primary"
          class="submit-btn"
          @click="resetPassword"
          :loading="loading"
        >
          {{ $t('sendInstructions') }}
        </el-button>
      </el-form>

      <div class="links-container">
        <p>
          {{ $t('rememberPassword') }}
          <el-link type="primary" @click="onLogin">{{ $t('login') }}</el-link>
        </p>
      </div>
    </div>

    <div class="lang-switch-container">
      <div class="lang-content">
        <button
          @click="changeLanguage('en')"
          :class="{ active: currentLanguage === 'en' }"
        >
          English
        </button>
        <span class="divider">|</span>
        <button
          @click="changeLanguage('zh')"
          :class="{ active: currentLanguage === 'zh' }"
        >
          中文
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/store/auth'
import logo from '@/assets/app_logo.png'

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
  padding-top: 4vh;
}

.box-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.logo-container {
  margin-bottom: 1rem;
}

.logo {
  max-height: 90px;
}

.title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.description {
  color: #606266;
  margin-bottom: 1.5rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.submit-btn {
  width: 100%;
}

.links-container {
  margin-top: 1.5rem;
}

/* Updated language switcher styles */
.lang-switch-container {
  background: #f0f2f5;
  width: 100%;
  padding: 1rem 0;
  margin-top: 2rem;
  border-top: 1px solid #e4e7ed;
}

.lang-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  max-width: 420px;
  margin: 0 auto;
}

.lang-content button {
  border: none;
  background: transparent;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0.25rem 0.5rem;
  color: #606266;
  transition: all 0.2s ease;
}

.lang-content button:hover {
  color: #409eff;
}

.lang-content button.active {
  color: #409eff;
}

.divider {
  color: #dcdfe6;
}
</style>