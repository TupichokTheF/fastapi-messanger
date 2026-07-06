<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { ApiError } from '../api/http'

const router = useRouter()
const { login } = useAuth()

const username = ref('')
const password = ref('')
const formError = ref('')
const submitting = ref(false)

async function onSubmit() {
  formError.value = ''
  if (!username.value.trim() || !password.value) {
    formError.value = 'Введите логин и пароль'
    return
  }
  submitting.value = true
  try {
    await login(username.value.trim(), password.value)
    router.push('/chats')
  } catch (err) {
    if (err instanceof ApiError && err.status === 401) {
      formError.value = 'Неверный логин или пароль'
    } else {
      formError.value = err?.detail || 'Не удалось войти'
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="auth-shell">
    <form class="auth-card" @submit.prevent="onSubmit" novalidate>
      <h1>Вход</h1>
      <p class="subtitle">С возвращением! Войдите в свой аккаунт.</p>

      <p v-if="formError" class="form-error">{{ formError }}</p>

      <div class="field">
        <label for="login-username">Имя пользователя</label>
        <input id="login-username" v-model="username" autocomplete="username" autofocus />
      </div>

      <div class="field">
        <label for="login-password">Пароль</label>
        <input
          id="login-password"
          v-model="password"
          type="password"
          autocomplete="current-password"
        />
      </div>

      <button class="btn-primary" type="submit" :disabled="submitting">
        {{ submitting ? 'Входим…' : 'Войти' }}
      </button>

      <p class="form-switch">
        Нет аккаунта?
        <RouterLink to="/register">Зарегистрироваться</RouterLink>
      </p>
    </form>
  </div>
</template>
