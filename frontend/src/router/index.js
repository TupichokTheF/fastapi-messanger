import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/LoginView.vue'
import Register from '../views/RegisterView.vue'
import Chat from '../views/ChatView.vue'

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/chat',
    component: Chat,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem('token')) next('/login')
      else next()
    },
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
