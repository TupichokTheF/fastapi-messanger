<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

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
    const res = await fetch('/api/v1/user/add_contact', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
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

let ws = null

const activeChatData = computed(() =>
  chats.value.find((c) => c.id === activeChat.value) || null
)

function connectWS() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  ws = new WebSocket(`${proto}://${location.host}/api/v1/ws/send_message?access_token=${token}`)
  ws.onmessage = (e) => {
    let msg
    try {
      msg = JSON.parse(e.data)
      if (typeof msg !== 'object' || !msg.content) msg = { content: e.data }
    } catch {
      msg = { content: e.data }
    }
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
}

function openChat(chatId) {
  activeContact.value = null
  activeChat.value = chatId
  messages.value = []
}

function sendMessage() {
  const text = newMessage.value.trim()
  if (!text || !ws || ws.readyState !== WebSocket.OPEN) return
  ws.send(text)
  newMessage.value = ''
}

async function createChat() {
  const name = newChatName.value.trim()
  if (!name) return
  try {
    const res = await fetch('/api/chats', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
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
  if (ws) ws.close()
  localStorage.removeItem('token')
  router.push('/login')
}

async function fetchContacts() {
  try {
    const res = await fetch('/api/v1/user/get_contacts', {
      headers: {
        'accept': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    })
    if (!res.ok) return
    const data = await res.json()
    contacts.value = data.contacts.map((c) => c.value)
  } catch {
    // handled silently
  }
}

onMounted(() => {
  connectWS()
  fetchContacts()
})
onUnmounted(() => {
  if (ws) ws.close()
})
</script>

<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="logo">Chat</span>
        <button class="icon-btn" title="Новый чат" @click="showNewChat = !showNewChat">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>

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
        <p class="list-label">Контакты</p>

        <button
          v-for="username in contacts"
          :key="username"
          class="chat-item"
          :class="{ active: username === activeContact }"
          @click="openContact(username)"
        >
          <span class="chat-avatar">{{ username[0].toUpperCase() }}</span>
          <span class="chat-name">{{ username }}</span>
        </button>

        <p v-if="contacts.length === 0" class="empty-hint">
          Нет контактов
        </p>
      </nav>

      <!-- Add user FAB -->
      <button class="fab" title="Добавить пользователя" @click="openAddUser">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        </svg>
      </button>

      <button class="logout-btn" @click="logout">
        <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
          <path d="M5 2H2a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h3M10 10l3-3-3-3M14 7.5H5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Выйти
      </button>
    </aside>

    <!-- Add user modal -->
    <Teleport to="body">
      <div v-if="showAddUser" class="modal-overlay" @click.self="showAddUser = false">
        <div class="modal">
          <div class="modal-header">
            <span class="modal-title">Добавить пользователя</span>
            <button class="modal-close" @click="showAddUser = false">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <form @submit.prevent="submitAddUser" novalidate>
            <div class="modal-field">
              <label for="addUsername">Имя пользователя</label>
              <input
                id="addUsername"
                v-model="addUsername"
                type="text"
                placeholder="your_username"
                autocomplete="off"
                autofocus
              />
            </div>

            <p v-if="addUserError" class="modal-error">{{ addUserError }}</p>

            <button type="submit" class="modal-btn" :disabled="addUserLoading">
              {{ addUserLoading ? 'Добавление...' : 'Добавить' }}
            </button>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Main area -->
    <main class="main">
      <template v-if="activeContact">
        <header class="chat-header">
          <div class="chat-header-avatar">{{ activeContact[0].toUpperCase() }}</div>
          <span class="chat-title">{{ activeContact }}</span>
        </header>

        <div class="messages" ref="messagesEl">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message"
            :class="{ own: msg.is_own }"
          >
            <span v-if="!msg.is_own" class="msg-author">{{ msg.author }}</span>
            <div class="msg-bubble">{{ msg.content }}</div>
            <span class="msg-time">{{ msg.created_at }}</span>
          </div>
        </div>

        <form class="input-bar" @submit.prevent="sendMessage">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Напишите сообщение..."
            autocomplete="off"
          />
          <button type="submit">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M9 15V3M3 9l6-6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </form>
      </template>

      <template v-else-if="activeChat">
        <header class="chat-header">
          <div class="chat-header-avatar">{{ activeChatData?.name[0].toUpperCase() }}</div>
          <span class="chat-title">{{ activeChatData?.name }}</span>
        </header>

        <div class="messages" ref="messagesEl">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message"
            :class="{ own: msg.is_own }"
          >
            <span v-if="!msg.is_own" class="msg-author">{{ msg.author }}</span>
            <div class="msg-bubble">{{ msg.content }}</div>
            <span class="msg-time">{{ msg.created_at }}</span>
          </div>
        </div>

        <form class="input-bar" @submit.prevent="sendMessage">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Напишите сообщение..."
            autocomplete="off"
          />
          <button type="submit">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M9 15V3M3 9l6-6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </form>
      </template>

      <div v-else class="placeholder">
        <div class="placeholder-inner">
          <div class="placeholder-icon">💬</div>
          <p>Выберите чат или создайте новый</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  background: #f0f0f0;
  color: #111;
  font-family: 'Inter', system-ui, sans-serif;
}

/* ── Sidebar ── */
.sidebar {
  width: 340px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-right: 1px solid #eee;
  position: relative;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 18px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.4px;
  color: #111;
}

.icon-btn {
  background: #f5f5f5;
  border: none;
  color: #111;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.icon-btn:hover { background: #ebebeb; }

.new-chat-form {
  padding: 12px 14px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  gap: 8px;
}

.new-chat-form input {
  flex: 1;
  background: #f7f7f7;
  border: 1.5px solid #ebebeb;
  color: #111;
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 10px;
  outline: none;
  min-width: 0;
  transition: border-color 0.15s;
}

.new-chat-form input:focus { border-color: #111; }

.btn-create {
  background: #111;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  padding: 0 14px;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s;
}

.btn-create:hover { background: #333; }

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 10px;
}

.chat-list::-webkit-scrollbar { width: 4px; }
.chat-list::-webkit-scrollbar-track { background: transparent; }
.chat-list::-webkit-scrollbar-thumb { background: #e0e0e0; border-radius: 4px; }

.chat-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  text-align: left;
  border-radius: 14px;
  transition: background 0.12s;
}

.chat-item:hover { background: #f5f5f5; color: #111; }
.chat-item.active { background: #f0f0f0; color: #111; }

.chat-avatar {
  width: 46px;
  height: 46px;
  background: #111;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  font-weight: 600;
  flex-shrink: 0;
}

.chat-name {
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #111;
}

.list-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #bbb;
  padding: 8px 10px 4px;
}

.empty-hint {
  padding: 28px 10px;
  font-size: 13px;
  color: #bbb;
  text-align: center;
}

.fab {
  position: absolute;
  bottom: 64px;
  left: 18px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #111;
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transition: background 0.15s, transform 0.1s;
  z-index: 10;
}

.fab:hover { background: #333; }
.fab:active { transform: scale(0.94); }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: #fff;
  border-radius: 20px;
  padding: 32px 32px 28px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.14);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.modal-title {
  font-size: 17px;
  font-weight: 700;
  color: #111;
  letter-spacing: -0.3px;
}

.modal-close {
  background: #f5f5f5;
  border: none;
  color: #555;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
}

.modal-close:hover { background: #ebebeb; color: #111; }

.modal-field {
  margin-bottom: 16px;
}

.modal-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #555;
  margin-bottom: 6px;
}

.modal-field input {
  width: 100%;
  background: #f7f7f7;
  border: 1.5px solid #ebebeb;
  color: #111;
  font-size: 14px;
  padding: 11px 14px;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}

.modal-field input:focus {
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0,0,0,0.06);
}

.modal-field input::placeholder { color: #bbb; }

.modal-error {
  font-size: 13px;
  color: #e53e3e;
  margin-bottom: 12px;
  padding: 9px 13px;
  background: #fff5f5;
  border-radius: 10px;
  border: 1px solid #fed7d7;
}

.modal-btn {
  width: 100%;
  padding: 12px;
  background: #111;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.15s, transform 0.1s;
  margin-top: 4px;
}

.modal-btn:hover:not(:disabled) { background: #333; }
.modal-btn:active:not(:disabled) { transform: scale(0.99); }
.modal-btn:disabled { opacity: 0.45; cursor: default; }

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  border-top: 1px solid #f0f0f0;
  color: #aaa;
  font-size: 13px;
  font-weight: 500;
  padding: 16px 18px;
  cursor: pointer;
  transition: color 0.15s;
  width: 100%;
  text-align: left;
}

.logout-btn:hover { color: #111; }

/* ── Main ── */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #f5f5f5;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: #fff;
  border-bottom: 1px solid #eee;
  flex-shrink: 0;
}

.chat-header-avatar {
  width: 36px;
  height: 36px;
  background: #111;
  color: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.chat-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.2px;
  color: #111;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.messages::-webkit-scrollbar { width: 4px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb { background: #ddd; border-radius: 4px; }

.message {
  display: flex;
  flex-direction: column;
  max-width: 58%;
  gap: 3px;
  align-self: flex-start;
}

.message.own {
  align-self: flex-end;
  align-items: flex-end;
}

.msg-author {
  font-size: 11px;
  font-weight: 600;
  color: #999;
  padding-left: 4px;
}

.msg-bubble {
  background: #fff;
  border: 1px solid #eee;
  padding: 10px 14px;
  border-radius: 16px;
  border-bottom-left-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
  color: #111;
  word-break: break-word;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.message.own .msg-bubble {
  background: #111;
  border-color: #111;
  color: #fff;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 4px;
}

.msg-time {
  font-size: 11px;
  color: #bbb;
  padding: 0 4px;
}

.input-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #fff;
  border-top: 1px solid #eee;
  flex-shrink: 0;
}

.input-bar input {
  flex: 1;
  background: #f5f5f5;
  border: 1.5px solid #ebebeb;
  color: #111;
  font-size: 14px;
  padding: 11px 16px;
  border-radius: 14px;
  outline: none;
  min-width: 0;
  transition: border-color 0.15s;
}

.input-bar input:focus { border-color: #111; }
.input-bar input::placeholder { color: #bbb; }

.input-bar button {
  background: #111;
  color: #fff;
  border: none;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  font-size: 18px;
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, transform 0.1s;
}

.input-bar button:hover { background: #333; }
.input-bar button:active { transform: scale(0.95); }

.placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-inner {
  text-align: center;
  color: #bbb;
}

.placeholder-icon {
  font-size: 40px;
  margin-bottom: 12px;
  filter: grayscale(1) opacity(0.5);
}

.placeholder-inner p {
  font-size: 14px;
  font-weight: 500;
}
</style>
