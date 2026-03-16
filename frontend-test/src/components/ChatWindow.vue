<template>
  <div class="bg-white rounded-xl shadow-lg flex flex-col h-[600px]">
    <!-- Messages area -->
    <div ref="messagesEl" class="flex-1 overflow-y-auto p-4 space-y-3">
      <MessageBubble
        v-for="(msg, i) in store.messages"
        :key="i"
        :message="msg"
      />
      <div v-if="store.isLoading" class="text-gray-400 text-sm animate-pulse pl-2">
        Думаю...
      </div>
    </div>

    <!-- Quick actions -->
    <QuickActions v-if="store.messages.length === 0" @action="sendQuickAction" />

    <!-- Input area -->
    <div class="border-t p-3 flex gap-2">
      <input
        v-model="inputText"
        @keydown.enter="sendMessage"
        :disabled="store.isLoading"
        placeholder="Напишите вопрос..."
        class="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        @click="sendMessage"
        :disabled="store.isLoading || !inputText.trim()"
        class="bg-blue-500 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-blue-600 disabled:opacity-50"
      >
        Отправить
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'
import { useChatStore } from '../stores/chat'
import { useChat } from '../composables/useChat'
import MessageBubble from './MessageBubble.vue'
import QuickActions from './QuickActions.vue'

const store = useChatStore()
const { sendMessageSSE } = useChat()
const inputText = ref('')
const messagesEl = ref(null)

store.initSession()

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || store.isLoading) return

  inputText.value = ''
  store.addUserMessage(text)
  store.isLoading = true

  store.messages.push({ role: 'assistant', text: '', cards: [], sources: [], timestamp: Date.now() })

  sendMessageSSE(
    text,
    store.sessionId,
    (delta) => store.appendDelta(delta),
    () => { store.isLoading = false },
    (cards) => {
      const last = store.messages[store.messages.length - 1]
      if (last) last.cards = cards
    }
  )
}

async function sendQuickAction(action) {
  try {
    const response = await axios.post('/chat/quick-action',
      { action },
      { headers: { Authorization: `Bearer ${localStorage.getItem('test_token') || 'test-token'}` } }
    )
    const message = response.data.message
    store.addUserMessage(message)
    store.isLoading = true
    store.messages.push({ role: 'assistant', text: '', cards: [], sources: [], timestamp: Date.now() })
    sendMessageSSE(message, store.sessionId,
      (delta) => store.appendDelta(delta),
      () => { store.isLoading = false },
      (cards) => { const last = store.messages[store.messages.length - 1]; if (last) last.cards = cards }
    )
  } catch (e) {
    console.error('Quick action failed:', e)
  }
}

watch(() => store.messages, async () => {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}, { deep: true })
</script>
