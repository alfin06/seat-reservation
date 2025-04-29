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
      <div class="translation-controls mb-2">
        <button @click="changeLanguage('en')" class="lang-btn">English</button>
        <button @click="changeLanguage('zh')" class="lang-btn">中文</button>
      </div>
      <footer class="footer">
        &copy; {{ new Date().getFullYear() }} Seat Reservation App | Developed by Inter Students
      </footer>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* full screen height */
}

/* Main content takes all available space */
.content-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center; /* Center if content is short, optional */
  padding: 20px;
}

/* Bottom controls always at bottom */
.bottom-controls {
  width: 100%;
  text-align: center;
  padding: 10px 0;
  background: #fff;
  border-top: 1px solid rgba(120, 130, 140, 0.13);
}

/* Footer styling */
.footer {
  color: #67757c;
  font-size: 14px;
}

/* Language buttons styling */
.translation-controls {
  margin-bottom: 10px;
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