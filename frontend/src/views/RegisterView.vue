<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { validateUsername, validatePassword, validateEmail } from '../utils/validation'

const router = useRouter()
const { register } = useAuth()

const username = ref('')
const email = ref('')
const password = ref('')

const formError = ref('')
const okMessage = ref('')
const submitting = ref(false)

async function onSubmit() {
  formError.value = ''
  okMessage.value = ''

  const uErr = validateUsername(username.value)
  const eErr = validateEmail(email.value)
  const pErr = validatePassword(password.value)
  if (uErr || eErr || pErr) {
    formError.value = uErr || eErr || pErr
    return
  }

  submitting.value = true
  try {
    const data = await register(username.value.trim(), email.value.trim(), password.value)
    okMessage.value = data?.detail || 'Регистрация успешна'
    // После регистрации — автопереход на вход.
    setTimeout(() => router.push('/login'), 700)
  } catch (err) {
    formError.value = err?.detail || 'Не удалось зарегистрироваться'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="auth-shell">
    <form class="auth-card" @submit.prevent="onSubmit" novalidate>
      <h1>Регистрация</h1>
      <p class="subtitle">Создайте аккаунт, чтобы начать переписку.</p>

      <p v-if="formError" class="form-error">{{ formError }}</p>
      <p v-if="okMessage" class="form-ok">{{ okMessage }}</p>

      <div class="field">
        <label for="reg-username">Имя пользователя</label>
        <input id="reg-username" v-model="username" autocomplete="username" autofocus />
        <p class="hint">От 6 до 20 символов</p>
      </div>

      <div class="field">
        <label for="reg-email">Email</label>
        <input id="reg-email" v-model="email" type="email" autocomplete="email" />
      </div>

      <div class="field">
        <label for="reg-password">Пароль</label>
        <input
          id="reg-password"
          v-model="password"
          type="password"
          autocomplete="new-password"
        />
        <p class="hint">Строчная и заглавная буквы, цифра</p>
      </div>

      <button class="btn-primary" type="submit" :disabled="submitting">
        {{ submitting ? 'Регистрируем…' : 'Зарегистрироваться' }}
      </button>

      <p class="form-switch">
        Уже есть аккаунт?
        <RouterLink to="/login">Войти</RouterLink>
      </p>
    </form>
  </div>
</template>

<style scoped>
.form-ok {
  background: #f0fdf4;
  color: var(--success);
  border: 1px solid #bbf7d0;
  border-radius: 10px;
  padding: 9px 12px;
  font-size: 13px;
  margin-bottom: 16px;
}
</style>
