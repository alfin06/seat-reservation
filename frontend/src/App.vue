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
    <!-- Main content (e.g., table, forms, etc.) -->
    <div class="content-container">
      <router-view />
    </div>
    <notifications position="top center" />
    <!-- Bottom controls: language translation controls -->
    <div class="bottom-controls">
      <div class="translation-controls">
        <button @click="changeLanguage('en')" class="lang-btn">English</button>
        <button @click="changeLanguage('zh')" class="lang-btn">中文</button>
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
  position: fixed;
  bottom: 20px;
}

.translation-controls {
  margin-top: 10px;
}

.lang-btn {
  margin: 0 5px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
}

.lang-btn:hover {
  background: #e9ecef;
}
</style>
