import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zh from './locales/zh.json'

// Configure i18n
const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en, zh },
  legacy: false
})

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.use(i18n)

app.mount('#app')
