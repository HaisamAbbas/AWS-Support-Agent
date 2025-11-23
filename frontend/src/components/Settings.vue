<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-[#1a1b26] rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-800">
      <!-- Header -->
      <div class="sticky top-0 bg-[#1a1b26] border-b border-gray-800 p-6 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-white">Settings</h2>
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6 space-y-6">
        <!-- Profile Section -->
        <div class="bg-[#16171f] rounded-xl p-6 border border-gray-800">
          <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Profile
          </h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Username</label>
              <input v-model="username" type="text" class="w-full bg-[#2d2e3f] text-white rounded-lg px-4 py-2 border border-gray-700 focus:border-purple-500 focus:outline-none transition-colors" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input v-model="email" type="email" class="w-full bg-[#2d2e3f] text-white rounded-lg px-4 py-2 border border-gray-700 focus:border-purple-500 focus:outline-none transition-colors" />
            </div>
          </div>
        </div>

        <!-- Preferences Section -->
        <div class="bg-[#16171f] rounded-xl p-6 border border-gray-800">
          <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
            Preferences
          </h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-white font-medium">Enable Streaming</p>
                <p class="text-sm text-gray-400">Show responses in real-time</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="enableStreaming" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-white font-medium">Include Sources</p>
                <p class="text-sm text-gray-400">Show document references</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="includeSources" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>
          </div>
        </div>

        <!-- Danger Zone -->
        <div class="bg-red-900/20 rounded-xl p-6 border border-red-500/30">
          <h3 class="text-lg font-semibold text-red-400 mb-4 flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Danger Zone
          </h3>
          <button @click="clearAllData" class="w-full bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg px-4 py-2 transition-colors">
            Clear All Chat History
          </button>
        </div>

        <!-- Save Button -->
        <button @click="saveSettings" class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-medium rounded-lg px-6 py-3 transition-all transform hover:scale-[1.02] active:scale-[0.98]">
          Save Settings
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineEmits(['close'])

const username = ref('User')
const email = ref('user@example.com')
const enableStreaming = ref(true)
const includeSources = ref(false)

onMounted(() => {
  loadSettings()
})

function loadSettings() {
  username.value = localStorage.getItem('username') || 'User'
  email.value = localStorage.getItem('userEmail') || 'user@example.com'
  enableStreaming.value = localStorage.getItem('enableStreaming') !== 'false'
  includeSources.value = localStorage.getItem('includeSources') === 'true'
}

function saveSettings() {
  localStorage.setItem('username', username.value)
  localStorage.setItem('userEmail', email.value)
  localStorage.setItem('enableStreaming', enableStreaming.value)
  localStorage.setItem('includeSources', includeSources.value)
  alert('Settings saved successfully!')
}

function clearAllData() {
  if (confirm('Are you sure you want to clear all chat history? This cannot be undone.')) {
    localStorage.removeItem('chat_history')
    alert('Chat history cleared!')
  }
}
</script>
