import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css' // Using the default Vite CSS. Replace with your own global styles.
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'

import { createI18n } from 'vue-i18n'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"

// Import locale files
import en from './locales/en.json'
import zh from './locales/zh.json'

// vue3-notification
import Notifications from '@kyvg/vue3-notification'

// Configure i18n
const i18n = createI18n({
    locale: 'en',
    fallbackLocale: 'en',
    messages: { en, zh }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(ElementPlus)
app.use(Notifications)

app.mount('#app')

const authStore = useAuthStore()
authStore.setCsrfToken()