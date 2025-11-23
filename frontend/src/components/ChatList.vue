<template>
  <div class="px-3 space-y-1">
    <!-- New Chat Button -->
    <button @click="$emit('new')" class="w-full flex items-center gap-3 px-3 py-2 text-purple-400 hover:text-purple-300 hover:bg-[#2d2e3f] rounded-lg transition-colors border border-purple-500/30 mb-3">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
      <span class="text-sm font-medium">New Chat</span>
    </button>

    <!-- Chat Items -->
    <div v-for="chat in chats" :key="chat.id" 
         @click="$emit('select', chat.id)"
         :class="[
           'w-full px-3 py-3 rounded-lg transition-all cursor-pointer group',
           activeChat === chat.id 
             ? 'bg-[#2d2e3f] border-l-2 border-purple-500' 
             : 'hover:bg-[#2d2e3f]/50'
         ]">
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-white text-sm font-medium truncate">{{ chat.name }}</p>
          <p class="text-gray-400 text-xs truncate mt-0.5">{{ chat.lastMessage || 'No messages yet' }}</p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="chats.length === 0" class="text-center py-8 text-gray-500">
      <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
      <p class="text-sm">No chats yet</p>
      <p class="text-xs mt-1">Click "New Chat" to start</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  chats: {
    type: Array,
    default: () => []
  },
  activeChat: {
    type: String,
    default: null
  }
})

defineEmits(['select', 'new'])
</script>
