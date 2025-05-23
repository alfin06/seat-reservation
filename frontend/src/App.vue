<template>
  <div class="app">
    <header class="app-header">
      <!-- Wrap the title in $t() for translation -->
      <h1>{{ $t('title') }}</h1>
      
      <nav class="main-nav">
        <router-link to="/register" class="nav-link">{{ $t('register') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/login" class="nav-link">{{ $t('login') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/reservation" class="nav-link">{{ $t('reservationTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/check-in" class="nav-link">{{ $t('checkInTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/instant-booking" class="nav-link">{{ $t('instantBookingTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/booking-history" class="nav-link">{{ $t('bookingHistory.title') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/admin-dashboard" class="nav-link">{{ $t('adminTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/general-settings" class="nav-link">{{ $t('generalSettingsTitle') }}</router-link>
      </nav>
    </header>

    <main class="app-content">
      <router-view />
    </main>

    <footer class="app-footer">
      <div class="language-toggle">
        <button 
          @click="changeLanguage('en')"
          :class="{ 'active': currentLanguage === 'en' }"
        >
          English
        </button>
        <span class="divider">|</span>
        <button 
          @click="changeLanguage('zh')"
          :class="{ 'active': currentLanguage === 'zh' }"
        >
          中文
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

const { locale } = useI18n()
const currentLanguage = ref(locale.value)

const changeLanguage = (lang) => {
  locale.value = lang
  currentLanguage.value = lang
}
</script>

<style scoped>
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}
.main-nav {
  margin-top: 1rem;
}
.nav-link {
  color: white;
  text-decoration: none;
  margin: 0 0.5rem;
}
.nav-divider {
  color: #ccc;
}
.app-content {
  padding: 2rem;
}
.app-footer {
  text-align: center;
  padding: 1rem;
  background-color: #f5f5f5;
}
.language-toggle button {
  border: none;
  background: none;
  cursor: pointer;
  font-weight: bold;
}
.language-toggle .active {
  text-decoration: underline;
}
.divider {
  margin: 0 0.5rem;
  color: #999;
}
</style>