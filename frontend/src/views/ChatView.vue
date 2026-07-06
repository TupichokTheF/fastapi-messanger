<script setup>
import { onMounted, ref } from 'vue'
import { useAuth } from '../composables/useAuth'
import { useChats } from '../composables/useChats'
import { useWebSocket } from '../composables/useWebSocket'
import ChatList from '../components/ChatList.vue'
import ChatWindow from '../components/ChatWindow.vue'
import NewChatModal from '../components/NewChatModal.vue'
import ConnectionBadge from '../components/ConnectionBadge.vue'

const { user, logout } = useAuth()
const { connect } = useWebSocket()
const {
  chats,
  activeChat,
  activeChatId,
  activeMessages,
  loadingChats,
  loadingMessages,
  currentUserId,
  loadChats,
  openChat,
  createDirectChat,
  send,
} = useChats()

const showNewChat = ref(false)

onMounted(async () => {
  // Один сокет на приложение; connect идемпотентен (не переоткрывает живой).
  connect()
  await loadChats()
})

function onSelect(chatId) {
  openChat(chatId)
}

async function onCreated({ value, resolve, reject }) {
  try {
    await createDirectChat(value)
    resolve()
  } catch (err) {
    reject(err)
  }
}
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <header class="sidebar-head">
        <div class="me">
          <span class="me-avatar">{{ (user?.username?.[0] || '?').toUpperCase() }}</span>
          <div class="me-meta">
            <span class="me-name">{{ user?.username || 'Гость' }}</span>
            <ConnectionBadge />
          </div>
        </div>
        <button class="icon-btn" title="Выйти" @click="logout">
          <svg width="18" height="18" viewBox="0 0 16 16" fill="none">
            <path
              d="M6 2H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3M11 11l3-3-3-3M14 8H6"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </header>

      <div class="new-chat-row">
        <button class="btn-primary" @click="showNewChat = true">Новый чат</button>
      </div>

      <ChatList
        :chats="chats"
        :active-chat-id="activeChatId"
        :loading="loadingChats"
        @select="onSelect"
      />
    </aside>

    <main class="main">
      <ChatWindow
        v-if="activeChat"
        :chat="activeChat"
        :messages="activeMessages"
        :current-user-id="currentUserId()"
        :loading="loadingMessages"
        @send="send"
      />
      <div v-else class="placeholder">
        <div class="placeholder-inner">
          <div class="mark">💬</div>
          <p>Выберите чат, чтобы начать переписку</p>
        </div>
      </div>
    </main>

    <NewChatModal v-if="showNewChat" @close="showNewChat = false" @created="onCreated" />
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  background: var(--surface);
}

.sidebar {
  width: 340px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-right: 1px solid var(--border);
}

.sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}

.me {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.me-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.me-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.me-name {
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.icon-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
  flex-shrink: 0;
}

.icon-btn:hover {
  background: var(--surface-2);
  color: var(--text);
}

.new-chat-row {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
}

.main {
  flex: 1;
  display: flex;
  min-width: 0;
}

.placeholder {
  flex: 1;
  display: grid;
  place-items: center;
  background: var(--surface-2);
}

.placeholder-inner {
  text-align: center;
  color: var(--text-muted);
}

.mark {
  font-size: 44px;
  margin-bottom: 12px;
}
</style>
