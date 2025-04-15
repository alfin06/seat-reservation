<template>
  <div class="app">
    <header class="app-header">
      <h1>{{ $t('title') }}</h1>
      <nav class="main-nav">
        <router-link to="/register" class="nav-link">{{ $t('register') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/login" class="nav-link">{{ $t('login') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/reservation" class="nav-link">{{ $t('reservationTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/checkin" class="nav-link">{{ $t('checkInTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/instant-booking" class="nav-link">{{ $t('instantBookingTitle') }}</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/admin" class="nav-link">{{ $t('adminTitle') }}</router-link>
      </nav>
    </header>

    <main class="app-content">
      <router-view />
    </main>

    <!-- Language Switcher -->
    <div class="translation-controls">
      <button @click="changeLanguage('en')">English</button>
      <button @click="changeLanguage('zh')">中文</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranslatedApp',
  methods: {
    changeLanguage(lang) {
      this.$i18n.locale = lang;
    }
  }
}
</script>

<style>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
}

.app-header h1 {
  font-size: 2rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.main-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.nav-link {
  font-weight: 600;
  color: #2c3e50;
  text-decoration: none;
  padding: 5px 10px;
}

.nav-link:hover {
  color: #646cff;
}

.nav-link.router-link-exact-active {
  color: #646cff;
  text-decoration: underline;
}

.nav-divider {
  color: #ccc;
  padding: 0 5px;
}

.app-content {
  padding: 20px 0;
}

/* Translation controls */
.translation-controls {
  text-align: center;
  margin-top: 20px;
}

.translation-controls button {
  margin: 0 5px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
