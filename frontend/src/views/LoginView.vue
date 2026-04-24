<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  if (!username.value.trim() || !password.value) {
    error.value = 'Заполните все поля'
    return
  }
  loading.value = true
  try {
    const res = await fetch('/api/v1/auth/sign_in', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username.value.trim(), password: password.value }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      error.value = data.detail || 'Неверный логин или пароль'
      return
    }
    const data = await res.json()
    localStorage.setItem('token', data.token)
    router.push('/chat')
  } catch {
    error.value = 'Ошибка соединения с сервером'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="card">
      <div class="brand">Chat</div>

      <form @submit.prevent="submit" novalidate>
        <input
          v-model="username"
          type="text"
          placeholder="Имя пользователя"
          autocomplete="username"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Пароль"
          autocomplete="current-password"
        />

        <button type="submit" class="btn" :disabled="loading || !username.trim() || !password">
          {{ loading ? 'Вход…' : 'Войти' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>

    <div class="card card-sub">
      Нет аккаунта?
      <RouterLink to="/register">Зарегистрироваться</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #fafafa;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
  color: #000;
}

.card {
  width: 100%;
  max-width: 360px;
  padding: 40px 32px 28px;
  background: #fff;
  border: 1px solid #dbdbdb;
  border-radius: 2px;
}

.card-sub {
  padding: 20px;
  text-align: center;
  font-size: 14px;
  color: #262626;
}

.card-sub a {
  color: #000;
  font-weight: 600;
  text-decoration: none;
  margin-left: 4px;
}

.card-sub a:hover { text-decoration: underline; }

.brand {
  font-size: 40px;
  font-weight: 800;
  letter-spacing: -1px;
  text-align: center;
  margin: 8px 0 28px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

input {
  width: 100%;
  background: #fafafa;
  border: 1px solid #dbdbdb;
  color: #000;
  font-size: 13px;
  padding: 11px 10px;
  border-radius: 3px;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  font-family: inherit;
}

input:focus { border-color: #a8a8a8; }
input::placeholder { color: #8e8e8e; }

.btn {
  margin-top: 10px;
  width: 100%;
  padding: 8px;
  background: #000;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.15s;
  font-family: inherit;
}

.btn:hover:not(:disabled) { opacity: 0.85; }
.btn:disabled { opacity: 0.35; cursor: default; }

.error {
  font-size: 13px;
  color: #000;
  text-align: center;
  margin: 14px 0 0;
  line-height: 1.4;
}
</style>
