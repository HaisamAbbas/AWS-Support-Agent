<template>
  <div class="flex flex-col h-full bg-[#1a1b26]">
    <!-- Header -->
    <div class="bg-[#16171f] border-b border-gray-800 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-bold text-white">Hi, I'm Chat Bot</h2>
          <p class="text-gray-400 text-sm mt-1">Tell me your goal, and get complete Learning Plans.</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="initializeAgent" :disabled="initializing" class="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg transition-all disabled:opacity-50 font-medium text-sm">
            {{ initializing ? '⏳ Initializing...' : '🚀 Initialize Agent' }}
          </button>
          <button @click="refreshStatus" class="p-2 text-gray-400 hover:text-white hover:bg-[#2d2e3f] rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Status Badge -->
      <div class="mt-3 flex items-center gap-2">
        <div :class="[
          'px-3 py-1 rounded-full text-xs font-medium flex items-center gap-2',
          status === 'ready' ? 'bg-green-500/20 text-green-400' :
          status === 'initializing' ? 'bg-yellow-500/20 text-yellow-400' :
          'bg-gray-500/20 text-gray-400'
        ]">
          <div class="w-2 h-2 rounded-full" :class="status === 'ready' ? 'bg-green-400' : status === 'initializing' ? 'bg-yellow-400 animate-pulse' : 'bg-gray-400'"></div>
          {{ statusText }}
        </div>
      </div>
    </div>

    <!-- Feature Cards -->
    <div class="px-6 py-4 border-b border-gray-800" v-if="messages.length === 0">
      <h3 class="text-center text-gray-400 italic text-sm mb-4">Here is what You'll get</h3>
      <div class="grid grid-cols-3 gap-3">
        <div v-for="feature in features" :key="feature.title" class="bg-[#16171f] rounded-xl p-4 border border-gray-800 hover:border-purple-500/30 transition-all">
          <div class="flex flex-col items-center text-center gap-2">
            <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', feature.bgColor]">
              <span class="text-xl">{{ feature.icon }}</span>
            </div>
            <div class="flex-1">
              <p class="text-white font-medium text-sm">{{ feature.title }}</p>
              <p class="text-gray-500 text-xs mt-1">{{ feature.percent }}</p>
            </div>
            <div :class="['w-full h-1 rounded-full', feature.barColor]"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages Area -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
      <div v-for="(m, idx) in messages" :key="idx" 
           :class="['flex', m.role === 'user' ? 'justify-end' : 'justify-start', 'animate-fadeIn']">
        <div :class="[
          'max-w-[70%] rounded-2xl px-4 py-3',
          m.role === 'user' ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white' : 
          m.role === 'system' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30' :
          'bg-[#16171f] text-gray-200 border border-gray-800'
        ]">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-semibold opacity-75">
              {{ m.role === 'user' ? '👤 You' : m.role === 'system' ? '⚙️ System' : '🤖 AI' }}
            </span>
            <span class="text-xs opacity-60">{{ m.time }}</span>
          </div>
          <div class="whitespace-pre-wrap text-sm leading-relaxed" v-html="formatMessage(m.text)"></div>
          <div v-if="m.streaming" class="mt-2 flex items-center gap-2 text-xs opacity-75">
            <div class="animate-pulse">●</div>
            <span>streaming...</span>
          </div>
        </div>
      </div>
      <div v-if="loading && !streamingActive" class="flex justify-start animate-pulse">
        <div class="bg-[#16171f] text-gray-200 rounded-2xl px-4 py-3 border border-gray-800">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-purple-600 rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            <span class="ml-2 text-sm">AI is thinking...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <form @submit.prevent="sendQuestion" class="border-t border-gray-800 p-6">
      <div class="flex items-end gap-3">
        <div class="flex-1 bg-[#2d2e3f] rounded-2xl px-4 py-3 border border-gray-700 focus-within:border-purple-500 transition-colors">
          <input 
            v-model="question" 
            placeholder="Enter your goal/prompts here............"
            class="w-full bg-transparent text-white placeholder-gray-500 focus:outline-none"
            @keydown.enter.exact.prevent="sendQuestion"
          />
          <div class="flex items-center gap-4 mt-2">
            <label class="flex items-center gap-2 cursor-pointer text-xs text-gray-400 hover:text-gray-300">
              <input type="checkbox" v-model="includeSources" class="w-3 h-3 text-purple-600 rounded focus:ring-purple-500" />
              <span>Include sources</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer text-xs text-gray-400 hover:text-gray-300">
              <input type="checkbox" v-model="useStreaming" class="w-3 h-3 text-purple-600 rounded focus:ring-purple-500" />
              <span>⚡ Stream</span>
            </label>
          </div>
        </div>
        <button type="submit" :disabled="!question.trim() || loading" class="p-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-2xl transition-all disabled:opacity-50 disabled:cursor-not-allowed">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue'
import { initializeAgent, queryAgent, queryAgentStreaming, getStatus } from '../api'

export default {
  name: 'Chat',
  props: {
    chatId: {
      type: String,
      default: 'default'
    }
  },
  emits: ['logout'],
  setup() {
    const messages = ref([])
    const question = ref('')
    const includeSources = ref(false)
    const useStreaming = ref(false)
    const loading = ref(false)
    const sending = ref(false)
    const initializing = ref(false)
    const status = ref('unknown')
    const statusText = ref('Unknown')
    const messagesContainer = ref(null)
    const streamingActive = ref(false)
    
    const features = [
      { icon: '👥', title: 'Guided Learning', percent: '15%', bgColor: 'bg-orange-500', barColor: 'bg-orange-500' },
      { icon: '🔗', title: 'Links To Course', percent: '63%', bgColor: 'bg-yellow-500', barColor: 'bg-yellow-500' },
      { icon: '💾', title: 'Save Courses', percent: '41%', bgColor: 'bg-cyan-500', barColor: 'bg-cyan-500' },
      { icon: '💬', title: 'Chat Wit AI', percent: '15%', bgColor: 'bg-pink-500', barColor: 'bg-pink-500' },
      { icon: '💡', title: 'Learning Plans', percent: '63%', bgColor: 'bg-green-500', barColor: 'bg-green-500' },
      { icon: '📥', title: 'Download PDFs', percent: '41%', bgColor: 'bg-purple-500', barColor: 'bg-purple-500' }
    ]

    const STORAGE_KEY = 'aws_agent_chat_history'

    const now = () => new Date().toLocaleTimeString()

    // Load chat history from localStorage
    function loadHistory() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY)
        if (stored) {
          messages.value = JSON.parse(stored)
        }
      } catch (err) {
        console.error('Failed to load chat history:', err)
      }
    }

    // Save chat history to localStorage
    function saveHistory() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.value))
      } catch (err) {
        console.error('Failed to save chat history:', err)
      }
    }

    // Clear chat history
    function clearHistory() {
      if (confirm('Clear all chat history?')) {
        messages.value = []
        localStorage.removeItem(STORAGE_KEY)
      }
    }

    // Auto-save on messages change
    watch(messages, () => {
      saveHistory()
    }, { deep: true })

    // Scroll to bottom
    async function scrollToBottom() {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    // Format message with basic markdown-like rendering
    function formatMessage(text) {
      return text
        .replace(/`([^`]+)`/g, '<code class="bg-gray-200 px-1 rounded">$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    }

    async function refreshStatus() {
      try {
        const s = await getStatus()
        status.value = s.initialized ? 'ready' : 'not_initialized'
        statusText.value = s.initialized ? `Ready (${s.llm_type})` : 'Not initialized'
      } catch (err) {
        status.value = 'error'
        statusText.value = 'Error'
        console.error(err)
      }
    }

    async function initializeAgentHandler() {
      initializing.value = true
      status.value = 'initializing'
      statusText.value = 'Initializing...'
      try {
        const resp = await initializeAgent()
        messages.value.push({ role: 'system', text: resp.message || 'Agent initialized successfully!', time: now() })
        await refreshStatus()
        scrollToBottom()
      } catch (err) {
        messages.value.push({ role: 'agent', text: '❌ Initialization failed: ' + (err.response?.data?.detail || err.message || err), time: now() })
        console.error(err)
        status.value = 'error'
        statusText.value = 'Error'
        scrollToBottom()
      } finally {
        initializing.value = false
      }
    }

    async function sendQuestion() {
      if (!question.value.trim()) return
      sending.value = true
      loading.value = true
      const q = question.value.trim()
      messages.value.push({ role: 'user', text: q, time: now() })
      question.value = ''
      scrollToBottom()

      try {
        if (useStreaming.value) {
          // Streaming mode
          streamingActive.value = true
          const msgIndex = messages.value.length
          messages.value.push({ role: 'agent', text: '', time: now(), streaming: true })
          
          await queryAgentStreaming(q, includeSources.value, (chunk) => {
            messages.value[msgIndex].text += chunk
            scrollToBottom()
          })
          
          messages.value[msgIndex].streaming = false
          streamingActive.value = false
        } else {
          // Regular mode
          const resp = await queryAgent(q, includeSources.value)
          messages.value.push({ role: 'agent', text: resp.response || String(resp), time: now() })
          if (resp.sources && resp.sources.length > 0) {
            messages.value.push({ role: 'agent', text: '📚 Sources: ' + resp.sources.join(', '), time: now() })
          }
        }
        scrollToBottom()
      } catch (err) {
        messages.value.push({ role: 'agent', text: '❌ Error: ' + (err.response?.data?.detail || err.message || err), time: now() })
        console.error(err)
        scrollToBottom()
      } finally {
        loading.value = false
        sending.value = false
        await refreshStatus()
      }
    }

    onMounted(() => {
      loadHistory()
      refreshStatus()
      scrollToBottom()
    })

    return {
      messages,
      question,
      includeSources,
      useStreaming,
      sendQuestion,
      loading,
      sending,
      initializeAgent: initializeAgentHandler,
      initializing,
      refreshStatus,
      status,
      statusText,
      messagesContainer,
      streamingActive,
      clearHistory,
      formatMessage,
      features
    }
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
</style>
