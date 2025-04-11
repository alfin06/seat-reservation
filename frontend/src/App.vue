<script>
export default {
  name: 'App',
  methods: {
    changeLanguage(lang) {
      this.$i18n.locale = lang;
    },
    onLogin() {
      // For example, redirect to the login page.
      this.$router.push('/login');
    }
  }
}
</script>

<template>
  <div class="app-container">
    <h1>{{ $t('title') }}</h1>
    <!-- <nav>
      <router-link to="/register">{{ $t('register') }}</router-link> |
      <router-link to="/login">{{ $t('login') }}</router-link> |
      <router-link to="/reservation">{{ $t('reservationTitle') }}</router-link> |
      <router-link to="/checkin">{{ $t('checkInTitle') }}</router-link> |
      <router-link to="/instant-booking">{{ $t('instantBookingTitle') }}</router-link> |
      <router-link to="/admin">{{ $t('adminTitle') }}</router-link>
    </nav> -->
    
    <!-- Main content (e.g., table, forms, etc.) -->
    <div class="content-container">
      <router-view />
    </div>
    
    <!-- Bottom controls: login button and language translation controls -->
    <div class="bottom-controls">
      <el-button type="primary" @click="onLogin">{{ $t('login') }}</el-button>
      <div class="translation-controls">
        <button @click="changeLanguage('en')">English</button>
        <button @click="changeLanguage('zh')">中文</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 100vh;
  padding: 20px;
}

nav a {
  margin: 0 10px;
}

.content-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

/* Bottom controls styling */
.bottom-controls {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.translation-controls {
  margin-top: 10px;
}

.translation-controls button {
  margin: 0 5px;
}
</style>
