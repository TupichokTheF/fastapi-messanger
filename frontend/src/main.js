import { createApp } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import './style.css'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()
  app.use(pinia)
  // Активная pinia нужна, чтобы дергать сторы вне компонентов (restore до mount).
  setActivePinia(pinia)

  // Тихая попытка восстановить сессию по refresh-cookie до монтирования,
  // чтобы навигационные гварды сразу знали статус авторизации.
  const auth = useAuthStore()
  await auth.restore()

  app.use(router)
  app.mount('#app')
}

bootstrap()
