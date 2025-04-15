import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createI18n } from 'vue-i18n'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// Import locale files
import en from './locales/en.json'
import zh from './locales/zh.json'

// Configure i18n
const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en, zh }
})

createApp(App)
  .use(router)
  .use(i18n)
  .use(ElementPlus)
  .mount('#app')
