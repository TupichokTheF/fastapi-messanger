<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../utils/api'

const router = useRouter()

const contacts = ref([])
const chats = ref([])
const activeChat = ref(null)
const activeContact = ref(null)
const messages = ref([])
const newMessage = ref('')
const newChatName = ref('')
const showNewChat = ref(false)
const showAddUser = ref(false)
const addUsername = ref('')
const addUserError = ref('')
const addUserLoading = ref(false)

function openAddUser() {
  addUsername.value = ''
  addUserError.value = ''
  showAddUser.value = true
}

async function submitAddUser() {
  addUserError.value = ''
  if (!addUsername.value.trim()) {
    addUserError.value = 'Введите имя пользователя'
    return
  }
  addUserLoading.value = true
  try {
    const res = await apiFetch('/api/v1/user/add_contact', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ contact_username: addUsername.value.trim() }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      addUserError.value = data.detail || 'Не удалось добавить пользователя'
      return
    }
    showAddUser.value = false
  } catch {
    addUserError.value = 'Ошибка соединения с сервером'
  } finally {
    addUserLoading.value = false
  }
}
const messagesEl = ref(null)
const token = localStorage.getItem('token')

function getUsernameFromToken(t) {
  if (!t) return ''
  try {
    const payload = JSON.parse(atob(t.split('.')[1]))
    return payload.sub || payload.username || ''
  } catch {
    return ''
  }
}
const currentUser = getUsernameFromToken(token)

let ws = null

const activeChatData = computed(() =>
  chats.value.find((c) => c.id === activeChat.value) || null
)

function disconnectWS() {
  if (!ws) return
  ws.onmessage = null
  ws.onclose = null
  ws.onerror = null
  if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
    ws.close()
  }
  ws = null
}

function connectWS() {
  disconnectWS()
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  ws = new WebSocket(`${proto}://${location.host}/api/v1/ws/send_message?access_token=${token}`)
  ws.onmessage = (e) => {
    let msg
    try {
      msg = JSON.parse(e.data)
    } catch {
      return
    }
    if (typeof msg !== 'object' || msg === null) return
    if (!activeContact.value || msg.spender !== activeContact.value) return
    messages.value.push(msg)
    scrollBottom()
  }
  ws.onclose = () => {}
  ws.onerror = () => {}
}

function openContact(username) {
  activeChat.value = null
  activeContact.value = username
  messages.value = []
  connectWS()
}

function openChat(chatId) {
  activeContact.value = null
  activeChat.value = chatId
  messages.value = []
  connectWS()
}

function sendMessage() {
  const text = newMessage.value.trim()
  if (!text || !activeContact.value || !ws || ws.readyState !== WebSocket.OPEN) return
  const created_at = new Date().toISOString()
  ws.send(JSON.stringify({
    text,
    receiver: activeContact.value,
    created_at,
  }))
  messages.value.push({
    text,
    spender: currentUser,
    receiver: activeContact.value,
    created_at,
  })
  scrollBottom()
  newMessage.value = ''
}

async function createChat() {
  const name = newChatName.value.trim()
  if (!name) return
  try {
    const res = await apiFetch('/api/chats', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name }),
    })
    const chat = await res.json()
    chats.value.push(chat)
    newChatName.value = ''
    showNewChat.value = false
    openChat(chat.id)
  } catch {
    // handled silently
  }
}

function scrollBottom() {
  nextTick(() => {
    if (messagesEl.value)
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  })
}

function logout() {
  disconnectWS()
  localStorage.removeItem('token')
  router.push('/login')
}

async function fetchContacts() {
  try {
    const res = await apiFetch('/api/v1/user/get_contacts', {
      headers: {
        'accept': 'application/json',
      },
    })
    if (!res.ok) return
    const data = await res.json()
    contacts.value = data.contacts.map((c) => c.value)
  } catch {
    // handled silently
  }
}

function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  if (isNaN(d)) return ''
  return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchContacts()
})
onUnmounted(() => {
  disconnectWS()
})
</script>

<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <header class="sidebar-header">
        <span class="brand">Chat</span>
        <div class="header-actions">
          <button class="icon-btn" title="Добавить пользователя" @click="openAddUser">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </button>
          <button class="icon-btn" title="Новый чат" @click="showNewChat = !showNewChat">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M4 16l2-5 8-8 3 3-8 8-5 2zM11 5l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </header>

      <div v-if="showNewChat" class="new-chat-form">
        <input
          v-model="newChatName"
          type="text"
          placeholder="Название чата"
          @keydown.enter="createChat"
          autofocus
        />
        <button class="btn-create" @click="createChat">Создать</button>
      </div>

      <nav class="chat-list">
        <button
          v-for="username in contacts"
          :key="username"
          class="chat-item"
          :class="{ active: username === activeContact }"
          @click="openContact(username)"
        >
          <span class="chat-avatar">{{ username[0].toUpperCase() }}</span>
          <span class="chat-meta">
            <span class="chat-name">{{ username }}</span>
            <span class="chat-sub">@{{ username }}</span>
          </span>
        </button>

        <p v-if="contacts.length === 0" class="empty-hint">
          Список контактов пуст
        </p>
      </nav>

      <footer class="sidebar-footer">
        <div class="me">
          <span class="me-avatar">{{ (currentUser[0] || '?').toUpperCase() }}</span>
          <span class="me-name">{{ currentUser || 'Гость' }}</span>
        </div>
        <button class="logout-btn" @click="logout" title="Выйти">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 2H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3M11 11l3-3-3-3M14 8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </footer>
    </aside>

    <!-- Add user modal -->
    <Teleport to="body">
      <div v-if="showAddUser" class="modal-overlay" @click.self="showAddUser = false">
        <div class="modal">
          <div class="modal-header">
            <span class="modal-title">Новый контакт</span>
            <button class="modal-close" @click="showAddUser = false" aria-label="Закрыть">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                <path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <form @submit.prevent="submitAddUser" novalidate>
            <input
              v-model="addUsername"
              type="text"
              placeholder="Имя пользователя"
              autocomplete="off"
              autofocus
            />

            <button type="submit" class="modal-btn" :disabled="addUserLoading">
              {{ addUserLoading ? 'Добавление…' : 'Добавить' }}
            </button>

            <p v-if="addUserError" class="modal-error">{{ addUserError }}</p>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Main area -->
    <main class="main">
      <template v-if="activeContact">
        <header class="chat-header">
          <div class="chat-header-avatar">{{ activeContact[0].toUpperCase() }}</div>
          <div class="chat-header-meta">
            <span class="chat-title">{{ activeContact }}</span>
            <span class="chat-status">в сети</span>
          </div>
        </header>

        <div class="messages" ref="messagesEl">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message"
            :class="{ own: msg.spender === currentUser }"
          >
            <div class="msg-bubble">{{ msg.text }}</div>
            <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>

        <form class="input-bar" @submit.prevent="sendMessage">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Сообщение"
            autocomplete="off"
          />
          <button type="submit" class="send-btn" :disabled="!newMessage.trim()">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M2 9l14-7-7 14-2-6-5-1z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
            </svg>
          </button>
        </form>
      </template>

      <template v-else-if="activeChat">
        <header class="chat-header">
          <div class="chat-header-avatar">{{ activeChatData?.name[0].toUpperCase() }}</div>
          <div class="chat-header-meta">
            <span class="chat-title">{{ activeChatData?.name }}</span>
            <span class="chat-status">групповой чат</span>
          </div>
        </header>

        <div class="messages" ref="messagesEl">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message"
            :class="{ own: msg.spender === currentUser }"
          >
            <span v-if="msg.spender !== currentUser" class="msg-author">{{ msg.spender }}</span>
            <div class="msg-bubble">{{ msg.text }}</div>
            <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>

        <form class="input-bar" @submit.prevent="sendMessage">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Сообщение"
            autocomplete="off"
          />
          <button type="submit" class="send-btn" :disabled="!newMessage.trim()">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M2 9l14-7-7 14-2-6-5-1z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
            </svg>
          </button>
        </form>
      </template>

      <div v-else class="placeholder">
        <div class="placeholder-inner">
          <div class="placeholder-mark">Chat</div>
          <p>Выберите контакт, чтобы начать переписку</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  background: #fff;
  color: #000;
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
}

/* ── Sidebar ── */
.sidebar {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-right: 1px solid #dbdbdb;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 18px;
  border-bottom: 1px solid #efefef;
}

.brand {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.6px;
  color: #000;
}

.header-actions {
  display: flex;
  gap: 4px;
}

.icon-btn {
  background: none;
  border: none;
  color: #000;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.icon-btn:hover { background: #f0f0f0; }
.icon-btn:active { background: #e4e4e4; }

.new-chat-form {
  padding: 10px 14px;
  border-bottom: 1px solid #efefef;
  display: flex;
  gap: 6px;
}

.new-chat-form input {
  flex: 1;
  background: #fafafa;
  border: 1px solid #dbdbdb;
  color: #000;
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 999px;
  outline: none;
  min-width: 0;
  transition: border-color 0.15s;
  font-family: inherit;
}

.new-chat-form input:focus { border-color: #a8a8a8; }
.new-chat-form input::placeholder { color: #8e8e8e; }

.btn-create {
  background: #000;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  padding: 0 14px;
  cursor: pointer;
  flex-shrink: 0;
  transition: opacity 0.15s;
  font-family: inherit;
}

.btn-create:hover { opacity: 0.85; }

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px 8px;
}

.chat-list::-webkit-scrollbar { width: 4px; }
.chat-list::-webkit-scrollbar-track { background: transparent; }
.chat-list::-webkit-scrollbar-thumb { background: #dbdbdb; border-radius: 4px; }

.chat-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 10px;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  border-radius: 10px;
  transition: background 0.12s;
  font-family: inherit;
}

.chat-item:hover { background: #f7f7f7; }
.chat-item.active { background: #efefef; }

.chat-avatar {
  width: 44px;
  height: 44px;
  background: #000;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.chat-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.chat-name {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.1px;
  color: #000;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-sub {
  font-size: 12px;
  color: #8e8e8e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-hint {
  padding: 28px 10px;
  font-size: 13px;
  color: #8e8e8e;
  text-align: center;
}

.sidebar-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-top: 1px solid #efefef;
  gap: 8px;
}

.me {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.me-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.me-name {
  font-size: 13px;
  font-weight: 600;
  color: #000;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-btn {
  background: none;
  border: none;
  color: #8e8e8e;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
  flex-shrink: 0;
}

.logout-btn:hover { background: #f0f0f0; color: #000; }

/* ── Modal ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: #fff;
  border: 1px solid #dbdbdb;
  border-radius: 2px;
  padding: 28px 28px 24px;
  width: 100%;
  max-width: 360px;
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 15px;
  font-weight: 700;
  color: #000;
  letter-spacing: -0.2px;
}

.modal-close {
  background: none;
  border: none;
  color: #000;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.modal-close:hover { background: #f0f0f0; }

.modal input {
  width: 100%;
  background: #fafafa;
  border: 1px solid #dbdbdb;
  color: #000;
  font-size: 13px;
  padding: 11px 12px;
  border-radius: 3px;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  font-family: inherit;
  margin-bottom: 12px;
}

.modal input:focus { border-color: #a8a8a8; }
.modal input::placeholder { color: #8e8e8e; }

.modal-error {
  font-size: 13px;
  color: #000;
  text-align: center;
  margin: 12px 0 0;
  line-height: 1.4;
}

.modal-btn {
  width: 100%;
  padding: 9px;
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

.modal-btn:hover:not(:disabled) { opacity: 0.85; }
.modal-btn:disabled { opacity: 0.35; cursor: default; }

/* ── Main ── */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #fff;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 24px;
  background: #fff;
  border-bottom: 1px solid #efefef;
  flex-shrink: 0;
}

.chat-header-avatar {
  width: 38px;
  height: 38px;
  background: #000;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.chat-header-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.chat-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.2px;
  color: #000;
}

.chat-status {
  font-size: 12px;
  color: #8e8e8e;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #fff;
}

.messages::-webkit-scrollbar { width: 4px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb { background: #dbdbdb; border-radius: 4px; }

.message {
  display: flex;
  flex-direction: column;
  max-width: 62%;
  gap: 2px;
  align-self: flex-start;
}

.message.own {
  align-self: flex-end;
  align-items: flex-end;
}

.msg-author {
  font-size: 11px;
  font-weight: 600;
  color: #8e8e8e;
  padding: 0 10px 2px;
}

.msg-bubble {
  background: #efefef;
  padding: 8px 14px;
  border-radius: 18px;
  border-bottom-left-radius: 4px;
  font-size: 14px;
  line-height: 1.35;
  color: #000;
  word-break: break-word;
}

.message.own .msg-bubble {
  background: #000;
  color: #fff;
  border-bottom-left-radius: 18px;
  border-bottom-right-radius: 4px;
}

.msg-time {
  font-size: 10px;
  color: #8e8e8e;
  padding: 0 10px;
  margin-top: 1px;
}

.input-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: #fff;
  border-top: 1px solid #efefef;
  flex-shrink: 0;
}

.input-bar input {
  flex: 1;
  background: #fafafa;
  border: 1px solid #dbdbdb;
  color: #000;
  font-size: 14px;
  padding: 10px 18px;
  border-radius: 999px;
  outline: none;
  min-width: 0;
  transition: border-color 0.15s;
  font-family: inherit;
}

.input-bar input:focus { border-color: #a8a8a8; }
.input-bar input::placeholder { color: #8e8e8e; }

.send-btn {
  background: #000;
  color: #fff;
  border: none;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.15s, transform 0.1s;
  font-family: inherit;
}

.send-btn:hover:not(:disabled) { opacity: 0.85; }
.send-btn:active:not(:disabled) { transform: scale(0.94); }
.send-btn:disabled { opacity: 0.25; cursor: default; }

.placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}

.placeholder-inner {
  text-align: center;
  color: #8e8e8e;
}

.placeholder-mark {
  font-size: 44px;
  font-weight: 800;
  letter-spacing: -1.2px;
  color: #000;
  margin-bottom: 10px;
}

.placeholder-inner p {
  font-size: 14px;
  font-weight: 500;
}
</style>
