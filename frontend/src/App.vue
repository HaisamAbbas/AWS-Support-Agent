<template>
  <div class="h-screen flex overflow-hidden bg-[#1a1b26]">
    <!-- Login Modal -->
    <Login v-if="showLogin" @authenticated="handleAuthenticated" @close="showLogin = false" />

    <!-- Left Sidebar -->
    <div v-if="isAuthenticated" class="w-64 bg-[#16171f] flex flex-col border-r border-gray-800">
      <!-- Logo/Brand -->
      <div class="p-4 border-b border-gray-800">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
            </svg>
          </div>
          <div>
            <h1 class="text-white font-bold text-lg">AWS Support Agent</h1>
          </div>
        </div>
      </div>

      <!-- Chats Section -->
      <div class="flex-1 overflow-y-auto">
        <div class="p-4">
          <button class="w-full bg-[#2d2e3f] hover:bg-[#373849] text-white rounded-lg px-4 py-3 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <span class="font-medium">Chats</span>
          </button>
        </div>

        <!-- Chat List -->
        <ChatList :chats="chatSessions" :activeChat="activeChatId" @select="selectChat" @new="createNewChat" />
      </div>

      <!-- Bottom: Settings & User -->
      <div class="border-t border-gray-800 p-4 space-y-2">
        <button @click="showSettings = true" class="w-full flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-[#2d2e3f] rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span class="text-sm font-medium">Settings</span>
        </button>
        
        <button @click="handleLogout" class="w-full flex items-center gap-3 px-3 py-2 text-gray-400 hover:text-white hover:bg-[#2d2e3f] rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="text-sm font-medium">Log Out</span>
        </button>

        <!-- User Profile -->
        <div class="flex items-center gap-3 px-3 py-2 bg-[#2d2e3f] rounded-lg mt-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center text-white font-bold">
            {{ username.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-white text-sm font-medium truncate">{{ username }}</p>
            <p class="text-gray-400 text-xs truncate">{{ userEmail }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div v-if="isAuthenticated" class="flex-1 flex flex-col">
      <Chat :chatId="activeChatId" @logout="handleLogout" />
    </div>

    <!-- Settings Modal -->
    <Settings v-if="showSettings" @close="showSettings = false" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chat from './components/Chat.vue'
import Login from './components/Login.vue'
import ChatList from './components/ChatList.vue'
import Settings from './components/Settings.vue'

const isAuthenticated = ref(false)
const showLogin = ref(false)
const showSettings = ref(false)
const activeChatId = ref('default')
const chatSessions = ref([
  { id: 'default', name: 'AWS Support Chat', lastMessage: 'Start chatting...', timestamp: new Date() }
])
const username = ref('User')
const userEmail = ref('user@example.com')

onMounted(() => {
  const apiKey = localStorage.getItem('api_key')
  if (apiKey) {
    isAuthenticated.value = true
    loadUserProfile()
  } else {
    showLogin.value = true
  }
})

function loadUserProfile() {
  const savedUsername = localStorage.getItem('username') || 'User'
  const savedEmail = localStorage.getItem('userEmail') || 'user@example.com'
  username.value = savedUsername
  userEmail.value = savedEmail
}

function handleAuthenticated() {
  isAuthenticated.value = true
  showLogin.value = false
  loadUserProfile()
}

function handleLogout() {
  localStorage.removeItem('api_key')
  localStorage.removeItem('username')
  localStorage.removeItem('userEmail')
  isAuthenticated.value = false
  showLogin.value = true
}

function selectChat(chatId) {
  activeChatId.value = chatId
}

function createNewChat() {
  const newChat = {
    id: `chat-${Date.now()}`,
    name: 'New Chat',
    lastMessage: '',
    timestamp: new Date()
  }
  chatSessions.value.unshift(newChat)
  activeChatId.value = newChat.id
}
</script>
