import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ChatView from '../views/ChatView.vue'

const routes = [
  { path: '/', redirect: '/chats' },
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/chats', name: 'chats', component: ChatView, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/chats' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Гварды: неавторизованных — на /login, авторизованных с /login|/register — на /chats.
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { path: '/login' }
  }
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { path: '/chats' }
  }
  return true
})

export default router
