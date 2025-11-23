<template>
  <div class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
    <div class="bg-[#1a1b26] rounded-2xl shadow-2xl max-w-md w-full p-8 animate-slideUp border border-gray-800">
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <svg class="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-white mb-2">Welcome to AWS Support Agent</h2>
        <p class="text-gray-400">Enter your API key to start learning</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">API Key</label>
          <input 
            v-model="apiKey" 
            type="password"
            placeholder="Enter your API key"
            class="w-full bg-[#2d2e3f] text-white rounded-lg px-4 py-3 border border-gray-700 focus:border-purple-500 focus:outline-none transition-colors placeholder-gray-500"
            required
            autofocus
          />
          <p class="mt-2 text-xs text-gray-500">
            💡 For demo: use "demo-key-123" or any 5+ characters
          </p>
        </div>

        <div v-if="error" class="bg-red-500/20 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <div class="flex gap-3">
          <button 
            type="submit" 
            :disabled="loading || !apiKey.trim()"
            class="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg px-6 py-3 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {{ loading ? '⏳ Logging in...' : '🔓 Login' }}
          </button>
          <button 
            type="button"
            @click="$emit('close')"
            class="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>

      <div class="mt-6 pt-6 border-t border-gray-800">
        <p class="text-xs text-gray-500 text-center">
          Don't have an API key? Contact your administrator or use the demo key above.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { login } from '../api'

export default {
  name: 'Login',
  emits: ['authenticated', 'close'],
  setup(props, { emit }) {
    const apiKey = ref('')
    const loading = ref(false)
    const error = ref('')

    async function handleLogin() {
      loading.value = true
      error.value = ''

      try {
        const result = await login(apiKey.value)
        
        if (result.success) {
          // Store API key in localStorage
          localStorage.setItem('api_key', apiKey.value)
          emit('authenticated')
        } else {
          error.value = result.message || 'Invalid API key'
        }
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Login failed'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    return {
      apiKey,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>
