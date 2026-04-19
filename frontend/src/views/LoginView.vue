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
      <div class="logo">Chat</div>

      <h1>Добро пожаловать</h1>
      <p class="subtitle">Войдите в свой аккаунт</p>

      <form @submit.prevent="submit" novalidate>
        <div class="field">
          <label for="username">Имя пользователя</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="your_username"
            autocomplete="username"
          />
        </div>

        <div class="field">
          <label for="password">Пароль</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
          />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <p class="footer">
        Нет аккаунта?
        <RouterLink to="/register">Зарегистрироваться</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 20px;
}

.card {
  width: 100%;
  max-width: 400px;
  padding: 48px 40px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.08);
}

.logo {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-bottom: 36px;
  color: #111;
}

h1 {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.4px;
  margin-bottom: 6px;
  color: #111;
}

.subtitle {
  font-size: 14px;
  color: #999;
  margin-bottom: 32px;
}

.field {
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #555;
  margin-bottom: 6px;
}

input {
  width: 100%;
  background: #f7f7f7;
  border: 1.5px solid #ebebeb;
  color: #111;
  font-size: 14px;
  padding: 12px 16px;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

input:focus {
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
}

input::placeholder {
  color: #bbb;
}

.error {
  font-size: 13px;
  color: #e53e3e;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: #fff5f5;
  border-radius: 10px;
  border: 1px solid #fed7d7;
}

.btn {
  width: 100%;
  padding: 13px;
  background: #111;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  letter-spacing: 0.02em;
  margin-top: 8px;
  transition: background 0.15s, transform 0.1s;
}

.btn:hover:not(:disabled) { background: #333; }
.btn:active:not(:disabled) { transform: scale(0.99); }
.btn:disabled { opacity: 0.45; cursor: default; }

.footer {
  margin-top: 24px;
  font-size: 13px;
  color: #999;
  text-align: center;
}

.footer a {
  color: #111;
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1.5px solid #ddd;
  padding-bottom: 1px;
  transition: border-color 0.15s;
}

.footer a:hover { border-color: #111; }
</style>
